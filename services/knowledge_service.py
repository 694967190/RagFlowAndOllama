import json
import httpx
import logging
import re
from config import settings
from models.schemas import ChatRequest, KnowledgeRequest
from .token_manager import token_manager

logger = logging.getLogger(__name__)

# 添加正则表达式模式
THINK_PATTERN = re.compile(r'<think>.*?</think>', re.DOTALL)

async def get_knowledge_base_response(question: str) -> str:
    """获取知识库响应"""
    logger.info("构建知识库请求")
    knowledge_request = KnowledgeRequest(
        question=question,
        kb_id=settings.KB_ID
    )
    
    # 获取有效的 token
    token = await token_manager.get_valid_token()
    headers = {
        "Authorization": token
    }
    
    timeout = httpx.Timeout(600.0)
    
    logger.info(f"开始请求知识库 URL: {settings.KNOWLEDGE_BASE_URL}")
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(
                settings.KNOWLEDGE_BASE_URL,
                json=knowledge_request.model_dump(),
                headers=headers
            )
            data = response.json()
            
            if data["code"] != 0:
                # 如果是token失效，尝试刷新token并重试
                if "token" in data.get("message", "").lower():
                    logger.info("Token 可能已失效，尝试刷新")
                    if await token_manager.refresh_token():
                        return await get_knowledge_base_response(question)
                
                logger.warning(f"知识库请求返回错误码: {data['code']}, 消息: {data.get('message', '')}")
                return ""
            
            logger.info(f"知识库返回 {len(data['data']['chunks'])} 条数据")
            
            knowledge = ""
            for chunk in data["data"]["chunks"]:
                knowledge += chunk["content_with_weight"] + "\n"
                logger.debug(f"处理数据块: {chunk['chunk_id']}, 相似度: {chunk['similarity']}")
            
            return knowledge
            
        except Exception as e:
            logger.error(f"请求知识库时发生错误: {str(e)}")
            raise

async def get_ollama_response(chat_request: ChatRequest, knowledge: str):
    """获取Ollama响应"""
    logger.info("构建 Ollama 请求")
    prompt = f"""你是一个智能助手，请总结知识库的内容来回答问题，请列举知识库中的数据详细回答。当所有知识库内容都与问题无关时，你的回答必须包括"知识库中未找到您要的答案！"这句话。回答需要考虑聊天历史。
    以下是知识库：
    {knowledge}
    以上是知识库。
    
    问题：{chat_request.messages[-1].content}
    """
    
    modified_request = chat_request.model_dump()
    modified_request["messages"][-1]["content"] = prompt
    
    timeout = httpx.Timeout(600.0)
    logger.info(f"开始请求 Ollama URL: {settings.OLLAMA_URL}")
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            if chat_request.stream:
                # 流式响应
                async with client.stream('POST', settings.OLLAMA_URL, json=modified_request) as response:
                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            chunk = json.loads(line)
                            # 过滤掉 think 标签及其内容
                            if 'message' in chunk and 'content' in chunk['message']:
                                chunk['message']['content'] = THINK_PATTERN.sub('', chunk['message']['content'])
                            logger.debug(f"Ollama 流式响应片段: {chunk}")
                            yield json.dumps(chunk) + "\n"
                        except json.JSONDecodeError as e:
                            logger.error(f"解析流式响应行时发生错误: {str(e)}")
                            logger.error(f"问题行内容: {line}")
                            continue
            else:
                # 普通响应
                response = await client.post(
                    settings.OLLAMA_URL,
                    json=modified_request
                )
                raw_content = response.content.decode('utf-8')
                logger.info("Ollama 原始响应内容:")
                logger.info("-" * 50)
                logger.info(raw_content)
                logger.info("-" * 50)
                
                # 获取最后一个完整的响应
                response_lines = raw_content.strip().split('\n')
                if len(response_lines) > 0:
                    last_response = json.loads(response_lines[-1])
                    # 过滤掉 think 标签及其内容
                    if 'message' in last_response and 'content' in last_response['message']:
                        last_response['message']['content'] = THINK_PATTERN.sub('', last_response['message']['content'])
                    logger.info("Ollama 最终响应内容:")
                    logger.info("-" * 50)
                    if 'message' in last_response:
                        logger.info(f"Role: {last_response['message'].get('role', 'unknown')}")
                        logger.info(f"Content: {last_response['message'].get('content', '')}")
                    logger.info(f"Done: {last_response.get('done', False)}")
                    logger.info("-" * 50)
                    yield json.dumps(last_response)
                else:
                    error_msg = "Ollama 返回空响应"
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                
        except Exception as e:
            logger.error(f"请求 Ollama 时发生错误: {str(e)}", exc_info=True)
            raise

async def get_ollama_models() -> list:
    """获取Ollama模型列表"""
    logger.info("开始获取 Ollama 模型列表")
    
    timeout = httpx.Timeout(30.0)  # 设置30秒超时
    models_url = f"{settings.OLLAMA_URL.replace('/chat', '/tags')}"
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.get(models_url)
            data = response.json()
            logger.info(f"成功获取到 {len(data.get('models', []))} 个模型")
            return data.get('models', [])
            
        except Exception as e:
            logger.error(f"获取 Ollama 模型列表时发生错误: {str(e)}", exc_info=True)
            raise 