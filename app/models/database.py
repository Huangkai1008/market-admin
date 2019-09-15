from tortoise import Tortoise

from app.core.config import DB_TYPE, USERNAME, PASSWORD, HOST, PORT, DATABASE

DB_URL = f'{DB_TYPE}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'


async def init():
    """初始化连接"""
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']}
    )


async def disconnect():
    """停止连接"""
    await Tortoise.close_connections()
