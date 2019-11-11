from typing import List

from fastapi import APIRouter, Query, Body, Path
from starlette.status import HTTP_201_CREATED
from tortoise.exceptions import OperationalError

from app.db.queries import category as category_api
from app.db.queries import brand as brand_api
from app.db.queries import store as store_api
from app.db.queries import product as product_api
from app.exceptions import BadRequestException
from app.models.product import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ItemCreate,
)


router = APIRouter()


@router.get('/', response_model=ProductList, summary='获取商品列表')
async def get_products(
    page: int = Query(1, ge=1), size: int = Query(10, ge=1), *, cat_id=Query(None, ge=1)
):
    """获取商品列表"""
    products, total = await product_api.get_products(page, size, cat_id=cat_id)
    response = ProductList(products=products, total=total)
    return response


@router.post(
    '/', response_model=ProductRead, status_code=HTTP_201_CREATED, summary='创建商品'
)
async def create_product(product_create: ProductCreate = Body(...)):
    """创建商品"""
    cat_id = product_create.cat_id
    category = await category_api.get_category(cat_id)
    if not category:
        raise BadRequestException('不存在的商品分类')

    brand_id = product_create.brand_id
    brand = await brand_api.get_brand(brand_id)
    if not brand:
        raise BadRequestException('不存在的商品品牌')

    store_id = product_create.store_id
    store = await store_api.get_store(store_id)
    if not store:
        raise BadRequestException('不存在的商铺')

    product = await product_api.create_product(product_create)
    return product


@router.put('/{product_id}', response_model=ProductRead, summary='修改商品')
async def update_product(
    product_id=Path(..., ge=1, description='商品id'),
    product_update: ProductUpdate = Body(...),
):
    """修改商品"""
    product = await product_api.get_product(product_id)
    if not product:
        raise BadRequestException('不存在的商品')

    product = await product_api.update_product(product_id, product_update)
    return product


@router.post('/{product_id}/items', summary='新增商品sku', status_code=HTTP_201_CREATED)
async def create_items(
    product_id=Path(..., ge=1, description='商品id'),
    item_bulk_create: List[ItemCreate] = Body(...),
):
    """新增商品sku"""
    product = await product_api.get_product(product_id)
    if not product:
        raise BadRequestException('不存在的商品')

    cat_id = product['cat_id'] if isinstance(product, dict) else product.cat_id
    category = await category_api.get_category(cat_id)
    if not category:
        raise BadRequestException('不存在的商品分类')

    try:
        await product_api.bulk_create_sku(product_id, item_bulk_create)
    except OperationalError:
        raise BadRequestException('创建sku错误')
    return dict()
