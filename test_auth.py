import asyncio
import httpx
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def login_and_get_authorization():
    """先登录获取token，然后获取Authorization"""
    # 登录数据
    login_data = {
        "email": "694967190@qq.com",
        "password": "Uw4Cft7Ap13hSAuZxCJpUQFqr8gO68ULiHMXN0S2yo9ZYt014KtepTFFeMWkS/m3rUf++75PZM7VMY8hO8SlbKQPTLv6/CVuGiXiIkXVaBQ9+DlCCJ17aSJmGzGIZtUqBe/4+GTQr1x8PgfacfjLZJOBHs5MjaFGe8MS9ciLwnN60deOZU5NRX8Qwd9vnYW7NEFs/KYADuWgHgO750WYfSe2GhUW6amao0wV8g+5hjPpckurKcg0GiydH8p02C2W/Xcoh0jm3nsyzREF+0o/FERmKoNoaAlA1Cc26NksI54BdwcTpTmmwpRjvWguktwh21AXrtcrRMx1PFgoLj3XXA=="
    }

    async with httpx.AsyncClient() as client:
        try:
            # 发送登录请求
            logger.info("开始登录")
            response = await client.post(
                'http://127.0.0.1/v1/user/login',
                json=login_data
            )
            logger.info(f"登录响应状态码: {response.status_code}")
            logger.info(f"响应头: {dict(response.headers)}")

            if response.status_code == 200:
                # 从响应头中获取 Authorization
                auth = response.headers.get('Authorization')
                if auth:
                    logger.info("从响应头中获取到 Authorization")
                    return auth
                else:
                    logger.error("响应头中没有找到 Authorization")
            else:
                logger.error(f"登录失败: {response.text}")

        except Exception as e:
            logger.error(f"登录过程中发生错误: {str(e)}")
            raise

async def main():
    auth = await login_and_get_authorization()
    if auth:
        logger.info("成功获取 Authorization")
        # 测试获取到的 Authorization
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": auth}
            response = await client.post(
                'http://127.0.0.1/v1/chunk/retrieval_test',
                headers=headers
            )
            logger.info(f"测试访问知识库响应: {response.status_code}")
            logger.info(f"响应内容: {response.text}")

        # 更新 .env 文件
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # 更新或添加 KNOWLEDGE_BASE_TOKEN
        auth_line_found = False
        for i, line in enumerate(lines):
            if line.startswith('KNOWLEDGE_BASE_TOKEN='):
                lines[i] = f'KNOWLEDGE_BASE_TOKEN={auth}\n'
                auth_line_found = True
                break
        
        if not auth_line_found:
            lines.append(f'KNOWLEDGE_BASE_TOKEN={auth}\n')
        
        with open('.env', 'w') as f:
            f.writelines(lines)
        logger.info("已更新 .env 文件中的 KNOWLEDGE_BASE_TOKEN")

if __name__ == "__main__":
    asyncio.run(main())