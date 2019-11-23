import traceback
from typing import Any, Union

from loguru import logger
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from fastapi.exceptions import RequestValidationError, HTTPException


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = None, headers: dict = None):
        super(BadRequestException, self).__init__(HTTP_400_BAD_REQUEST, detail, headers)


class InvalidSystemClockException(Exception):
    """系统时钟错误"""

    pass


class GetHardwareIdFailedException(Exception):
    """获取系统硬件信息错误"""

    pass


async def page_not_found_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """page not found"""
    logger.warning(exc.detail)
    return JSONResponse(dict(message='page not found'), status_code=exc.status_code)


async def bad_request_handler(_: Request, exc: BadRequestException) -> JSONResponse:
    """Bad Request"""
    logger.warning(exc.detail)
    return JSONResponse(dict(message=exc.detail), status_code=HTTP_400_BAD_REQUEST)


async def validation_exception_handler(
    _: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """前端输入实体错误"""
    errors = exc.errors()
    message = errors[0]['msg']
    logger.warning(errors)

    return JSONResponse(
        dict(message=message), status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


async def server_error_handler(_: Request, __: HTTPException) -> JSONResponse:
    """服务器错误"""
    logger.error('Server Error')
    logger.warning(traceback.format_exc())
    return JSONResponse(
        dict(message='server error'), status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )
