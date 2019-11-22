import uvicorn

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from app.core.config import PROJECT_NAME, VERSION
from app.core.events import startup, shutdown
from app.api import api_router
from app.exceptions import BadRequestException

app = FastAPI(title=PROJECT_NAME)

app.include_router(api_router)


@app.exception_handler(HTTP_404_NOT_FOUND)
async def page_not_found(request, exc):
    """page not found"""

    return JSONResponse(dict(message='page not found'), status_code=exc.status_code)


@app.exception_handler(BadRequestException)
async def bad_request_handler(request, exc):
    """Bad Request"""
    return JSONResponse(dict(message=exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """验证前端输入实体"""
    errors = exc.errors()
    message = errors[0]['msg']

    return JSONResponse(
        dict(message=message), status_code=HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.exception_handler(HTTP_500_INTERNAL_SERVER_ERROR)
async def server_error(request, exc):
    return JSONResponse(
        dict(message='server error'), status_code=HTTP_500_INTERNAL_SERVER_ERROR
    )


def get_application() -> FastAPI:
    """Application Factory"""
    application = FastAPI(title=PROJECT_NAME, version=VERSION)

    application.add_event_handler('startup', startup)
    application.add_event_handler('shutdown', shutdown)
    return application


app = get_application()

uvicorn.run(app, host='0.0.0.0', port=8000)
