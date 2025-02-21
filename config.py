from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KB_ID: str = ""
    KNOWLEDGE_BASE_URL: str = "http://127.0.0.1/v1/chunk/retrieval_test"
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_MODEL: str = "llama2"
    KNOWLEDGE_BASE_TOKEN: str = ""
    
    # 添加登录相关配置
    LOGIN_URL: str = "http://127.0.0.1/v1/user/login"
    LOGIN_EMAIL: str = ""
    LOGIN_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings() 