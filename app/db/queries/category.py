from tortoise.queryset import QuerySet, Q

from app.db.category import ProductCategory
from app.db.queries import utils


async def get_categories(page: int, size: int, *, parent_id: int) -> QuerySet:
    """获取商品分类"""
    conditions = dict()

    if parent_id is not None:
        conditions['parent_id'] = parent_id

    queryset = await utils.and_pagination(
        ProductCategory.filter(**conditions), page, size
    )
    return queryset
