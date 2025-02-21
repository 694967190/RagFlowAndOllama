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
# 知识库配置
KB_ID=<你的知识库ID>                    # RAGFlow中的知识库ID
KNOWLEDGE_BASE_URL=http://127.0.0.1/v1/chunk/retrieval_test  # 知识库检索接口地址

# Ollama配置
OLLAMA_MODEL=llama2                    # Ollama模型名称
OLLAMA_URL=http://localhost:11434/api/chat  # Ollama API地址

# 认证配置（可选）
LOGIN_URL=http://127.0.0.1/v1/user/login  # 登录接口地址
LOGIN_EMAIL=<你的邮箱>                   # 登录邮箱
LOGIN_PASSWORD=<你的密码>                # 登录密码
KNOWLEDGE_BASE_TOKEN=<认证token>         # 知识库认证token 填写登录邮箱和密码后自动更新
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