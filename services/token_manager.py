import asyncio
import httpx
import logging
from config import settings

logger = logging.getLogger(__name__)

class TokenManager:
    def __init__(self):
        self._token = settings.KNOWLEDGE_BASE_TOKEN
        self._lock = asyncio.Lock()
        
    @property
    def token(self):
        return self._token
        
    async def refresh_token(self):
        """刷新token"""
        async with self._lock:  # 防止并发刷新
            try:
                # 登录数据
                login_data = {
                    "email": settings.LOGIN_EMAIL,
                    "password": settings.LOGIN_PASSWORD
                }

                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        settings.LOGIN_URL,
                        json=login_data
                    )

                    if response.status_code == 200:
                        new_token = response.headers.get('Authorization')
                        if new_token:
                            logger.info("成功获取新的 token")
                            self._token = new_token
                            return True
                    
                    logger.error(f"刷新 token 失败: {response.text}")
                    return False
                    
            except Exception as e:
                logger.error(f"刷新 token 时发生错误: {str(e)}")
                return False

    async def get_valid_token(self):
        """获取有效的token，如果当前token无效则刷新"""
        if not self._token:
            await self.refresh_token()
        return self._token

# 创建全局的 token 管理器实例
token_manager = TokenManager() 