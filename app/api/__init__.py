from fastapi import APIRouter

from app.api.v1.endpoints import index, category


api_router = APIRouter()

api_router.include_router(index.router, tags=['index'])
api_router.include_router(category.router, prefix='/categories', tags=['category'])
