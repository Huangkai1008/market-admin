from typing import Tuple, List

from app.db.queries import utils
from app.db.store import Store
from app.models.store import StoreCreate

from fastapi.encoders import jsonable_encoder


async def get_stores(page: int, size: int) -> Tuple[List[Store], int]:
    """获取商铺列表"""
    conditions = dict()

    total = await Store.filter(**conditions).count()
    queryset = await utils.and_pagination(Store.filter(**conditions), page, size)
    return queryset, total


async def get_store(store_id: int) -> Store:
    """获取单个商铺"""
    store = await Store.filter(id=store_id).first()
    return store


async def create_store(store_create: StoreCreate) -> Store:
    """创建商铺"""
    create_store_data = jsonable_encoder(store_create)
    store = Store(**create_store_data)
    await store.save()
    return store
