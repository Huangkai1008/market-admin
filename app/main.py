from fastapi import FastAPI

from .models import database
from .core.config import PROJECT_NAME
from .routers import index

app = FastAPI(title=PROJECT_NAME)

app.include_router(index.router)


@app.on_event('startup')
async def startup():
    await database.init()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
