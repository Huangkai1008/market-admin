from fastapi import APIRouter, Query, Body
from starlette.status import HTTP_201_CREATED

from app.db.queries import brand as brand_api
from app.models.brand import BrandList, BrandRead, BrandCreate

router = APIRouter()


@router.get('/', response_model=BrandList, summary='获取商品品牌列表')
async def get_brands(page: int = Query(1, ge=1), size: int = Query(10, ge=10)):
    """获取商品品牌列表"""
    brands, total = await brand_api.get_brands(page, size)
    response = BrandList(brands=brands, total=total)
    return response


@router.post(
    '/', response_model=BrandRead, status_code=HTTP_201_CREATED, summary='创建商品品牌'
)
async def create_brand(brand_create: BrandCreate = Body(...)):
    """创建商品品牌"""
    brand = brand_api.create_brand(brand_create)
    return brand
