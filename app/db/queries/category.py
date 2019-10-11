from fastapi.encoders import jsonable_encoder
from tortoise.queryset import QuerySet

from app.db.category import ProductCategory
from app.db.queries import utils
from app.models.category import CategoryCreate


async def get_categories(page: int, size: int, *, parent_id: int) -> QuerySet:
    """获取商品分类"""
    conditions = dict()

    if parent_id is not None:
        conditions['parent_id'] = parent_id

    queryset = await utils.and_pagination(
        ProductCategory.filter(**conditions), page, size
    )
    return queryset


async def get_category(cat_id):
    """获取单个商品分类"""
    queryset = await ProductCategory.get(id=cat_id)
    return queryset


async def create_category(category_create: CategoryCreate) -> ProductCategory:
    """创建商品分类"""
    category_create_data = jsonable_encoder(category_create)
    category = ProductCategory(**category_create_data)
    await category.save()
    return category
