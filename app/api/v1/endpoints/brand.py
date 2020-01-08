from fastapi import APIRouter, Query, Body, Depends
from starlette.status import HTTP_201_CREATED

from app.db.repositories.brand import BrandRepository
from app.models.brand import BrandList, BrandRead, BrandCreate

router = APIRouter()


@router.get('/', response_model=BrandList, summary='获取商品品牌列表')
async def get_brands(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=10),
    brand_repo: BrandRepository = Depends(BrandRepository),
):
    """获取商品品牌列表"""
    brands, total = await brand_repo.get_brands(page, size)
    response = BrandList(brands=brands, total=total)
    return response


@router.post(
    '/', response_model=BrandRead, status_code=HTTP_201_CREATED, summary='创建商品品牌'
)
async def create_brand(
    brand_create: BrandCreate = Body(...), brand_repo: BrandRepository = Depends()
):
    """创建商品品牌"""
    brand = await brand_repo.create_brand(brand_create)
    return brand
