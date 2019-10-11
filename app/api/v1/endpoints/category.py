from typing import List

from fastapi import APIRouter, Query, Body

from app.db.queries import category as category_api
from app.models.category import CategoryRead, CategoryCreate


router = APIRouter()


@router.get('/', response_model=List[CategoryRead])
async def get_product_categories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    *,
    parent_id: int = Query(0, ge=0)
):
    """获取产品分类列表"""
    categories = await category_api.get_categories(page, size, parent_id=parent_id)

    return categories


@router.post('/', response_model=CategoryRead)
async def create_product_category(category_create: CategoryCreate = Body(...)):
    """创建产品分类"""
    parent_id = category_create.parent_id  # 获取父分类

    if parent_id == 0:  # 为一级分类
        cat_level = 0
    else:
        parent_category = await category_api.get_category(parent_id)
        cat_level = parent_category.cat_level

    category_create.cat_level = cat_level

    category = await category_api.create_category(category_create)
    return category
