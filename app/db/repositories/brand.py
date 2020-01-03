from typing import Tuple, List

from fastapi.encoders import jsonable_encoder

from app.db.brand import Brand
from app.db.repositories.base import BaseRepository
from app.models.brand import BrandCreate


class BrandRepository(BaseRepository):
    """
    品牌Repo
    """

    async def get_brands(self, page: int, size: int) -> Tuple[List[Brand], int]:
        """获取商品品牌"""
        conditions = dict()

        total = await Brand.filter(**conditions).count()

        queryset = await self._and_pagination(Brand.filter(**conditions), page, size)
        return queryset, total

    @staticmethod
    async def get_brand(brand_id: int) -> Brand:
        """获取单个商品品牌"""
        brand = await Brand.filter(id=brand_id).first()
        return brand

    @staticmethod
    async def create_brand(brand_create: BrandCreate) -> Brand:
        """新增商品品牌"""
        create_brand_data = jsonable_encoder(brand_create)
        brand = Brand(**create_brand_data)
        await brand.save()
        return brand
