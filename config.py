from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KB_ID: str = "fb0f617ae96111efa7160242ac120006"
    KNOWLEDGE_BASE_URL: str = "http://127.0.0.1/v1/chunk/retrieval_test"
    OLLAMA_URL: str = "http://localhost:11434/api/chat"
    OLLAMA_MODEL: str = "llama2"
    KNOWLEDGE_BASE_TOKEN: str = ""
    
    # 添加登录相关配置
    LOGIN_URL: str = "http://127.0.0.1/v1/user/login"
    LOGIN_EMAIL: str = "694967190@qq.com"
    LOGIN_PASSWORD: str = "Uw4Cft7Ap13hSAuZxCJpUQFqr8gO68ULiHMXN0S2yo9ZYt014KtepTFFeMWkS/m3rUf++75PZM7VMY8hO8SlbKQPTLv6/CVuGiXiIkXVaBQ9+DlCCJ17aSJmGzGIZtUqBe/4+GTQr1x8PgfacfjLZJOBHs5MjaFGe8MS9ciLwnN60deOZU5NRX8Qwd9vnYW7NEFs/KYADuWgHgO750WYfSe2GhUW6amao0wV8g+5hjPpckurKcg0GiydH8p02C2W/Xcoh0jm3nsyzREF+0o/FERmKoNoaAlA1Cc26NksI54BdwcTpTmmwpRjvWguktwh21AXrtcrRMx1PFgoLj3XXA=="
    
    class Config:
        env_file = ".env"

settings = Settings() 