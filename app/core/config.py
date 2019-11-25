import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

from app.core.logging import InterceptHandler

config = Config('../.env')

# ================ Project ================
API_PREFIX = '/api'
VERSION = 'v1'
PROJECT_NAME: str = config('PROJECT_NAME', cast=str)

# ================ Mysql ================
DB_TYPE: str = config('DB_TYPE')
DB_USER: str = config('DB_USERNAME')
DB_PASSWORD: Secret = config('DB_PASSWORD', cast=Secret)
DB_HOST: str = config('DB_HOST')
DB_PORT: int = config('DB_PORT', cast=int)
DATABASE: str = config('DB_DATABASE')

# ================ Logging ================
LOGGING_LEVEL: str = config('LOGGING_LEVEL', cast=str, default='INFO')
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{'sink': sys.stderr, 'level': LOGGING_LEVEL}])
