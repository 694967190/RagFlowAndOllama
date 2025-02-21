# RagFlowAndOllama

## 项目简介

RagFlowAndOllama 是一个中继服务项目，旨在为Chatbox等Gpt-Gui提供调用Ollama大模型时添加知识库检索功能。该项目实现了RAG（检索增强生成）流程，通过结合本地知识库的内容来增强大模型的回答质量。

## 项目产生原因
由于RAGFlow的聊天功能太多问题，特此开发此项目
项目原理是使用了ragflow的检索接口通过用户输入的数据在本地知识库中进行相似度检索，然后根据检索到的内容生成提示词，最后调用Ollama大模型生成回答。

## 主要功能

1. 接收用户输入并保持与Ollama API兼容的请求格式
2. 基于用户输入在本地知识库中进行相似度检索
3. 将检索到的知识库内容与用户问题组合，生成优化的提示词
4. 调用Ollama大模型生成回答
5. 保持与Ollama API一致的返回格式

## 项目运行前提
1.装有RAGFlow，并且运行在本地
2.装有Ollama，并且运行在本地
RAGFlow-git链接 https://github.com/infiniflow/ragflow
Ollama-git链接 https://github.com/ollama/ollama

## 技术架构

### API接口

#### 1. 用户输入接口
```json
{
    "model": "<model-name>",
    "messages": [
        {
            "role": "user",
            "content": "<input-text>"
        }
    ],
    "stream": false,
    "options": {
        "temperature": 0.7,
        "max_tokens": 123456
    }
}
```

#### 2. 知识库检索接口
- 端点：`http://127.0.0.1/v1/chunk/retrieval_test`
- 方法：POST
- 参数示例：
```json
{
    "similarity_threshold": 0.2,
    "vector_similarity_weight": 0.8,
    "use_kg": false,
    "question": "<用户问题>",
    "doc_ids": [],
    "kb_id": "<知识库ID>",
    "page": 1,
    "size": 10
}
```

## 配置说明

项目配置信息存储在`.env`文件中，包括：
- 知识库ID (KB_ID)
- Ollama模型名称 (MODEL_NAME)
- Ollama服务地址 (MODEL_URL)

## 注意事项
- 确保本地知识库服务正常运行
- 正确配置环境变量
- 检查Ollama服务的可用性

## 项目运行

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 运行项目
```bash
python main.py
```

