from fastapi import FastAPI

from .routers import index

app = FastAPI()


app.include_router(index.router)
