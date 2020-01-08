from typing import List

from fastapi import APIRouter, Query, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.db.repositories.category import CategoryRepository
from app.api.dependencies.category import (
    get_category_by_id,
    get_category_spec_by_union_id,
)
from app.db.category import ProductCategory, ProductCategorySpec
from app.models.category import (
    CategoryRead,
    CategoryList,
    CategoryCreate,
    CategoryUpdate,
    CategorySpec,
    CategorySpecCreate,
    CategorySpecUpdate,
)


router = APIRouter()


@router.get('/', response_model=CategoryList, summary='获取商品分类列表')
async def get_product_categories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    category_repo: CategoryRepository = Depends(),
    *,
    parent_id: int = Query(0, ge=0)
):
    """获取商品分类列表"""
    categories, total = await category_repo.get_categories(
        page, size, parent_id=parent_id
    )

    response = CategoryList(categories=categories, total=total)

    return response


@router.post(
    '/', response_model=CategoryRead, status_code=HTTP_201_CREATED, summary='创建商品分类'
)
async def create_product_category(
    category_create: CategoryCreate = Body(...),
    category_repo: CategoryRepository = Depends(),
):
    """创建商品分类"""
    parent_id = category_create.parent_id  # 获取父分类

    if parent_id == 0:  # 为一级分类
        cat_level = 0
    else:
        parent_category = await category_repo.get_category(parent_id)
        cat_level = parent_category.cat_level + 1

    category = await category_repo.create_category(category_create, cat_level=cat_level)
    return category


@router.put('/{cat_id}', response_model=CategoryRead, summary='修改商品分类')
async def update_product_category(
    current_category: ProductCategory = Depends(get_category_by_id),
    category_update: CategoryUpdate = Body(...),
    category_repo: CategoryRepository = Depends(),
):
    """修改商品分类"""
    cat_id = current_category.id

    update_category = await category_repo.update_category(cat_id, category_update)
    return update_category


@router.get(
    '/{cat_id}/specs', response_model=List[CategorySpec], summary='查看商品分类下的规格信息'
)
async def get_category_specs(
    current_category: ProductCategory = Depends(get_category_by_id),
    category_repo: CategoryRepository = Depends(),
):
    """查看商品分类下的规格信息"""
    cat_id = current_category.id

    specs = await category_repo.get_category_specs(cat_id)
    return specs


@router.post('/{cat_id}/specs', status_code=HTTP_201_CREATED, summary='新增商品分类下的规格信息')
async def create_category_specs(
    current_category: ProductCategory = Depends(get_category_by_id),
    spec_creates: List[CategorySpecCreate] = Body(...),
    category_repo: CategoryRepository = Depends(),
):
    """新增商品分类下的规格信息"""
    cat_id = current_category.id

    await category_repo.bulk_create_category_specs(cat_id, spec_creates)
    return dict()


@router.put(
    '/{cat_id}/specs/{spec_id}', response_model=CategorySpec, summary='修改商品分类下的规格信息'
)
async def update_category_spec(
    current_category_spec: ProductCategorySpec = Depends(get_category_spec_by_union_id),
    spec_update: CategorySpecUpdate = Body(...),
    category_repo: CategoryRepository = Depends(),
):
    """修改商品分类下的规格信息"""
    spec_id = current_category_spec.id

    spec = await category_repo.update_category_spec(spec_id, spec_update)
    return spec
