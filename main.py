# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

from fastapi import FastAPI, HTTPException
import logging
from datetime import datetime
from models.schemas import ChatRequest, ChatResponse
from services.knowledge_service import get_knowledge_base_response, get_ollama_response, get_ollama_models
from config import settings
from fastapi.responses import StreamingResponse

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# 设置 httpx 的日志级别为 INFO
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()



@app.post("/api/chat")
async def chat(request: ChatRequest):
    request_id = datetime.now().strftime("%Y%m%d%H%M%S")
    logger.info(f"Request {request_id} - 收到新的聊天请求: {request.model}")
    
    try:
        # 获取用户问题
        user_question = request.messages[-1].content
        logger.info(f"Request {request_id} - 用户问题: {user_question}")
        
        # 获取知识库响应
        logger.info(f"Request {request_id} - 开始查询知识库")
        knowledge = await get_knowledge_base_response(user_question)
        logger.info(f"Request {request_id} - 知识库查询完成，获取到 {len(knowledge)} 字符的内容")
        
        # 获取Ollama响应
        logger.info(f"Request {request_id} - 开始请求 Ollama 模型")
        
        if request.stream:
            # 流式响应
            return StreamingResponse(
                get_ollama_response(request, knowledge),
                media_type="text/event-stream"
            )
        else:
            # 普通响应
            response = await get_ollama_response(request, knowledge)
            logger.info(f"Request {request_id} - Ollama 响应完成")
            return response
            
    except Exception as e:
        logger.error(f"Request {request_id} - 处理请求时发生错误: {str(e)}", exc_info=True)
        raise

@app.get("/api/chat/api/tags")
async def get_models():
    """获取可用的模型列表"""
    try:
        models = await get_ollama_models()
        return {
            "models": models
        }
    except Exception as e:
        logger.error(f"获取模型列表时发生错误: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    logger.info("服务启动")
    uvicorn.run(app, host="127.0.0.1", port=8000)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
