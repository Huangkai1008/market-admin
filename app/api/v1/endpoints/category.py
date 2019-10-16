from fastapi import APIRouter, Query, Body, Path
from starlette.status import HTTP_201_CREATED

from app.db.queries import category as category_api
from app.exceptions import BadRequestException
from app.models.category import (
    CategoryRead,
    CategoryList,
    CategoryCreate,
    CategoryUpdate,
)


router = APIRouter()


@router.get('/', response_model=CategoryList)
async def get_product_categories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    *,
    parent_id: int = Query(0, ge=0)
):
    """获取产品分类列表"""
    categories, total = await category_api.get_categories(
        page, size, parent_id=parent_id
    )

    response = CategoryList(categories=categories, total=total)

    return response


@router.post('/', response_model=CategoryRead, status_code=HTTP_201_CREATED)
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


@router.put('/{cat_id}', response_model=CategoryRead)
async def update_product_category(
    cat_id=Path(..., title='产品分类id', ge=1), category_update: CategoryUpdate = Body(...)
):
    """修改产品分类"""
    category = await category_api.get_category(cat_id)
    if not category:
        raise BadRequestException('不存在的产品分类')

    update_category = await category_api.update_category(cat_id, category_update)
    return update_category
