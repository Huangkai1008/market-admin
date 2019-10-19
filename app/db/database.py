from tortoise import Tortoise

from app.core.config import DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DATABASE

DB_URL = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'


async def init():
    """初始化连接"""
    await Tortoise.init(
        db_url=DB_URL,
        modules={
            'db': ['app.db.category', 'app.db.brand', 'app.db.store', 'app.db.product']
        },
    )
    await Tortoise.generate_schemas()


async def disconnect():
    """停止连接"""
    await Tortoise.close_connections()
