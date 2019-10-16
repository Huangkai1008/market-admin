from typing import List, Tuple

from fastapi.encoders import jsonable_encoder

from app.db.category import ProductCategory, ProductCategorySpec
from app.db.queries import utils
from app.models.category import (
    CategoryCreate,
    CategoryUpdate,
    CategorySpecCreate,
    CategorySpecUpdate,
)


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
    queryset = await ProductCategory.filter(id=cat_id).first()
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


async def get_category_specs(cat_id: int) -> List[ProductCategorySpec]:
    """获取规格信息"""
    conditions = dict()

    conditions['cat_id'] = cat_id

    queryset = await ProductCategorySpec.filter(**conditions).all()
    return queryset


async def get_category_spec(spec_id: int) -> ProductCategorySpec:
    """获取单个规格信息"""
    queryset = await ProductCategorySpec.filter(id=spec_id).first()
    return queryset


async def bulk_create_category_specs(
    cat_id: int, spec_creates: List[CategorySpecCreate]
):
    """批量创建规格信息"""
    spec_creates_data = jsonable_encoder(spec_creates)

    await ProductCategorySpec.bulk_create(
        [
            ProductCategorySpec(**spec_create_data, cat_id=cat_id)
            for spec_create_data in spec_creates_data
        ]
    )
    return


async def update_category_spec(
    spec_id: int, spec_update: CategorySpecUpdate
) -> ProductCategorySpec:
    """修改商品分类"""
    spec_update_data = jsonable_encoder(spec_update)
    await ProductCategorySpec.get(id=spec_id).update(**spec_update_data)
    spec = await get_category_spec(spec_id)
    return spec
