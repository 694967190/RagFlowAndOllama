# RagFlowAndOllama

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![RAGFlow](https://img.shields.io/badge/RAGFlow-Latest-green.svg)](https://github.com/infiniflow/ragflow)
[![Ollama](https://img.shields.io/badge/Ollama-Latest-orange.svg)](https://github.com/ollama/ollama)

</div>

## 📖 项目简介

RagFlowAndOllama 是一个智能中继服务项目，为Chatbox等GPT图形界面工具提供知识库增强的Ollama调用能力。该项目实现了RAG（检索增强生成）流程，通过结合本地知识库的内容来提升大模型的回答质量。

## 🎯 项目特点

- 完全兼容Ollama API的请求和响应格式
- 无缝集成RAGFlow的知识库检索能力
- 支持可配置的相似度阈值和权重
- 提供标准化的错误处理和响应机制

## ⚙️ 运行环境

### 前置依赖

1. [RAGFlow](https://github.com/infiniflow/ragflow)
   - 需在本地运行RAGFlow服务
   - 提供知识库检索能力

2. [Ollama](https://github.com/ollama/ollama)
   - 需在本地部署Ollama服务
   - 提供大模型推理能力

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件并配置以下参数：
```env
# RAGFlow配置
KB_ID=<你的知识库ID>                    # RAGFlow中的知识库ID
RAGFLOW_URL=http://127.0.0.1           # RAGFlow服务地址
RAGFLOW_PORT=80                        # RAGFlow服务端口

# Ollama配置
MODEL_NAME=qwen                        # Ollama模型名称，例如：qwen, llama2等
MODEL_URL=http://127.0.0.1:11434      # Ollama服务地址和端口

# 服务配置
HOST=127.0.0.1                        # 服务监听地址
PORT=8000                             # 服务监听端口
DEBUG=True                            # 调试模式开关

# 检索配置
SIMILARITY_THRESHOLD=0.2               # 相似度阈值
VECTOR_SIMILARITY_WEIGHT=0.8           # 向量相似度权重
RETRIEVAL_TOP_K=5                     # 检索返回的最大结果数
```

### 3. 运行服务

```bash
python main.py
```

## 📡 API接口

### 1. 用户查询接口

- 方法：`POST`
- 格式：与Ollama API保持一致

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

### 2. 知识库检索接口

- 端点：`http://127.0.0.1/v1/chunk/retrieval_test`
- 方法：`POST`

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

## 🔍 工作流程

1. 接收用户输入
2. 调用RAGFlow知识库检索接口
3. 处理检索结果并生成优化提示词
4. 调用Ollama模型生成回答
5. 返回标准格式响应

## ⚠️ 注意事项

- 确保RAGFlow服务正常运行
- 验证Ollama服务可用性
- 正确配置环境变量
- 定期检查知识库状态

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 📄 许可证

[MIT License](LICENSE)