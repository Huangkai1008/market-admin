from loguru import logger

from app.db import database


async def startup():
    await database.init()


@logger.catch
async def shutdown():
    await database.disconnect()
