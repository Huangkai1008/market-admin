from typing import List

from fastapi import APIRouter

from app.db.queries import category as category_api
from app.models.category import ProductCategory


router = APIRouter()


@router.get('/', response_model=List[ProductCategory])
async def get_product_categories(page: int = 1, size: int = 10, *, parent_id: int = 0):
    """获取产品分类列表"""
    categories = await category_api.get_categories(page, size, parent_id=parent_id)
    return categories
