from typing import List

from fastapi import APIRouter, Query

from app.db.queries import category as category_api
from app.models.category import ProductCategory


router = APIRouter()


@router.get('/', response_model=List[ProductCategory])
async def get_product_categories(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    *,
    parent_id: int = Query(0, ge=0)
):
    """获取产品分类列表"""
    categories = await category_api.get_categories(page, size, parent_id=parent_id)
    return categories
