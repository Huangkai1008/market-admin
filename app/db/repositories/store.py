from typing import Tuple, List

from fastapi.encoders import jsonable_encoder

from app.db.repositories.base import BaseRepository
from app.db.store import Store
from app.models.store import StoreCreate


class StoreRepository(BaseRepository):
    """
    商铺Repo
    """

    async def get_stores(self, page: int, size: int) -> Tuple[List[Store], int]:
        """获取商铺列表"""
        conditions = dict()

        total = await Store.filter(**conditions).count()
        queryset = await self._and_pagination(Store.filter(**conditions), page, size)
        return queryset, total

    @staticmethod
    async def get_store(store_id: int) -> Store:
        """获取单个商铺"""
        store = await Store.filter(id=store_id).first()
        return store

    @staticmethod
    async def create_store(store_create: StoreCreate) -> Store:
        """创建商铺"""
        create_store_data = jsonable_encoder(store_create)
        store = Store(**create_store_data)
        await store.save()
        return store
