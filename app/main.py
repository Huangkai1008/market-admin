import uvicorn

from fastapi import FastAPI

from app.models import database
from app.core.config import PROJECT_NAME
from app.routers import index

app = FastAPI(title=PROJECT_NAME)

app.include_router(index.router)


@app.on_event('startup')
async def startup():
    await database.init()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

uvicorn.run(app, host='0.0.0.0', port=8000)
