from typing import Any

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class BadRequestException(HTTPException):
    def __init__(self, detail: Any = None, headers: dict = None):
        super(BadRequestException, self).__init__(HTTP_400_BAD_REQUEST, detail, headers)
