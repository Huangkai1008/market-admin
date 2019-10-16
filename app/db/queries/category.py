from typing import List, Tuple

from fastapi.encoders import jsonable_encoder

from app.db.category import ProductCategory
from app.db.queries import utils
from app.models.category import CategoryCreate, CategoryUpdate


async def get_categories(
    page: int, size: int, *, parent_id: int
) -> Tuple[List[ProductCategory], int]:
    """获取商品分类"""
    conditions = dict()

    if parent_id is not None:
        conditions['parent_id'] = parent_id

    total = await ProductCategory.filter(**conditions).count()

    queryset = await utils.and_pagination(
        ProductCategory.filter(**conditions), page, size
    )

    return queryset, total


async def get_category(cat_id: int) -> ProductCategory:
    """获取单个商品分类"""
    queryset = await ProductCategory.get(id=cat_id)
    return queryset


async def create_category(category_create: CategoryCreate) -> ProductCategory:
    """创建商品分类"""
    category_create_data = jsonable_encoder(category_create, by_alias=False)
    category = ProductCategory(**category_create_data)
    await category.save()
    return category


async def update_category(
    cat_id: int, category_update: CategoryUpdate
) -> ProductCategory:
    """修改商品分类"""
    category_update_data = jsonable_encoder(category_update)
    await ProductCategory.get(id=cat_id).update(**category_update_data)
    category = await get_category(cat_id)
    return category
