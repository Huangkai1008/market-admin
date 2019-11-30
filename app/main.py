from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from app.core.config import PROJECT_NAME, VERSION, API_PREFIX
from app.core.events import startup, shutdown
from app.exceptions import (
    page_not_found_handler,
    bad_request_handler,
    validation_exception_handler,
    server_error_handler,
    BadRequestException,
)
from app.api import api_router


def get_application() -> FastAPI:
    """Application Factory"""
    application = FastAPI(title=PROJECT_NAME, version=VERSION)

    application.add_event_handler('startup', startup)
    application.add_event_handler('shutdown', shutdown)

    application.add_exception_handler(HTTP_404_NOT_FOUND, page_not_found_handler)
    application.add_exception_handler(BadRequestException, bad_request_handler)
    application.add_exception_handler(
        RequestValidationError, validation_exception_handler
    )
    application.add_exception_handler(
        HTTP_500_INTERNAL_SERVER_ERROR, server_error_handler
    )

    application.include_router(api_router, prefix=API_PREFIX)
    return application


app = get_application()
