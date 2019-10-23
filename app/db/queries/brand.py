from typing import List, Tuple

from fastapi.encoders import jsonable_encoder

from app.db.brand import Brand
from app.db.queries import utils
from app.models.brand import BrandCreate


async def get_brands(page: int, size: int) -> Tuple[List[Brand], int]:
    """获取商品品牌"""
    conditions = dict()

    total = await Brand.filter(**conditions).count()

    queryset = await utils.and_pagination(Brand.filter(**conditions), page, size)
    return queryset, total


async def get_brand(brand_id: int) -> Brand:
    """获取单个商品品牌"""
    queryset = await Brand.filter(id=brand_id).first()
    return queryset


async def create_brand(brand_create: BrandCreate) -> Brand:
    """新增商品品牌"""
    create_brand_data = jsonable_encoder(brand_create)
    brand = Brand(**create_brand_data)
    await brand.save()
    return brand
