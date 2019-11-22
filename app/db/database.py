from tortoise import Tortoise
from loguru import logger

from app.core.config import DB_TYPE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DATABASE

DB_URL = f'{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DATABASE}'


async def init():
    """初始化连接"""
    logger.info(f'Connecting to database')

    await Tortoise.init(
        db_url=DB_URL,
        modules={
            'db': ['app.db.category', 'app.db.brand', 'app.db.store', 'app.db.product']
        },
    )

    logger.info(f'Connection established')

    await Tortoise.generate_schemas()

    logger.info(f'Schema generated')


async def disconnect():
    """停止连接"""
    logger.info('Closing connection to database')

    await Tortoise.close_connections()

    logger.info('Connection closed')
