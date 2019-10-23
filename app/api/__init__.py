from fastapi import APIRouter

from app.api.v1.endpoints import index, category, brand, store, product


api_router = APIRouter()

api_router.include_router(index.router, tags=['index'])
api_router.include_router(category.router, prefix='/categories', tags=['category'])
api_router.include_router(brand.router, prefix='/brands', tags=['brand'])
api_router.include_router(store.router, prefix='/stores', tags=['store'])
api_router.include_router(product.router, prefix='/products', tags=['product'])
