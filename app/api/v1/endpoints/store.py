from fastapi import APIRouter, Query, Body
from starlette.status import HTTP_201_CREATED

from app.db.queries import store as store_api
from app.models.store import StoreRead, StoreList, StoreCreate

router = APIRouter()


@router.get('/', response_model=StoreList, summary='获取商铺列表')
async def get_stores(page: int = Query(1, ge=1), size: int = Query(10, ge=1)):
    """获取商铺列表"""
    stores, total = await store_api.get_stores(page, size)
    response = StoreList(stores=stores, total=total)
    return response


@router.post(
    '/', response_model=StoreRead, status_code=HTTP_201_CREATED, summary='创建商铺'
)
async def create_store(store_create: StoreCreate = Body(...)):
    """创建商铺"""
    store = await store_api.create_store(store_create)
    return store
