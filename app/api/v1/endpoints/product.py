from typing import List
from operator import attrgetter
from itertools import groupby

from fastapi import APIRouter, Query, Body, Path, Depends
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_201_CREATED
from tortoise.exceptions import OperationalError

from app.api.dependencies.product import (
    get_product_by_id,
    get_item_by_id,
    get_item_spec_by_id,
)
from app.db.repositories.brand import BrandRepository
from app.db.repositories.category import CategoryRepository
from app.db.repositories.product import ProductRepository
from app.db.repositories.store import StoreRepository
from app.db.product import Spu, Item, ItemSpec
from app.exceptions import BadRequestException
from app.models.product import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ItemCreate,
    ItemUpdate,
    ItemSpecCreate,
    ItemSpecUpdate,
)


router = APIRouter()


@router.get('/', response_model=ProductList, summary='获取商品列表')
async def get_products(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    product_repo: ProductRepository = Depends(),
    *,
    cat_id=Query(None, ge=1)
):
    """获取商品列表"""
    products, total = await product_repo.get_products(page, size, cat_id=cat_id)
    response = ProductList(products=products, total=total)
    return response


@router.post(
    '/', response_model=ProductRead, status_code=HTTP_201_CREATED, summary='创建商品'
)
async def create_product(
    product_create: ProductCreate = Body(...),
    brand_repo: BrandRepository = Depends(),
    category_repo: CategoryRepository = Depends(),
    store_repo: StoreRepository = Depends(),
    product_repo: ProductRepository = Depends(),
):
    """创建商品"""
    cat_id = product_create.cat_id
    category = await category_repo.get_category(cat_id)
    if not category:
        raise BadRequestException('不存在的商品分类')

    brand_id = product_create.brand_id
    brand = await brand_repo.get_brand(brand_id)
    if not brand:
        raise BadRequestException('不存在的商品品牌')

    store_id = product_create.store_id
    store = await store_repo.get_store(store_id)
    if not store:
        raise BadRequestException('不存在的商铺')

    product = await product_repo.create_product(product_create)
    return product


@router.put('/{product_id}', response_model=ProductRead, summary='修改商品')
async def update_product(
    current_product: Spu = Depends(get_product_by_id),
    product_update: ProductUpdate = Body(...),
    product_repo: ProductRepository = Depends(),
):
    """修改商品"""
    product_id = current_product.id

    product = await product_repo.update_product(product_id, product_update)
    return product


@router.get('/{product_id}/items', summary='查看商品sku')
async def get_items(
    product_id: int = Path(..., ge=1, description='商品id'),
    product_repo: ProductRepository = Depends(),
):
    product = await product_repo.get_product(product_id)
    if not product:
        raise BadRequestException('不存在的商品')

    items, _ = await product_repo.get_items()
    item_ids = [item.id for item in items]
    item_specs = await product_repo.get_item_specs(item_ids=item_ids, item_id_sort=True)
    spec_item_group = groupby(item_specs, key=attrgetter('item_id'))
    item_spec_map = {str(item_id): list(group) for item_id, group in spec_item_group}

    entities = list()
    for item in items:
        entity = jsonable_encoder(item)
        entity['specs'] = item_spec_map.get(str(item.id), [])
        entities.append(entity)
    return entities


@router.post('/{product_id}/items', summary='新增商品sku', status_code=HTTP_201_CREATED)
async def create_items(
    current_product: dict = Depends(get_product_by_id),
    item_bulk_create: List[ItemCreate] = Body(...),
    category_repo: CategoryRepository = Depends(),
    product_repo: ProductRepository = Depends(),
):
    """新增商品sku"""

    product_id = current_product['id']
    cat_id = current_product['cat_id']

    category = await category_repo.get_category(cat_id)
    if not category:
        raise BadRequestException('不存在的商品分类')

    try:
        await product_repo.bulk_create_sku(product_id, item_bulk_create)
    except OperationalError:
        raise BadRequestException('创建sku错误')
    return dict()


@router.put('/{product_id}/items/{item_id}', summary='修改商品sku')
async def update_items(
    _: dict = Depends(get_product_by_id),
    current_item: Item = Depends(get_item_by_id),
    item_update: ItemUpdate = Body(...),
    product_repo: ProductRepository = Depends(),
):
    """修改商品sku"""
    item_id = current_item.id

    item = await product_repo.update_item(item_id, item_update)
    return item


@router.post('/{product_id}/items/{item_id}/specs', summary='增加商品规格')
async def create_item_spec(
    _: dict = Depends(get_product_by_id),
    current_item: Item = Depends(get_item_by_id),
    spec_create: ItemSpecCreate = Body(...),
    product_repo: ProductRepository = Depends(),
):
    """新增sku规格"""
    item_id = current_item.id

    spec = await product_repo.create_item_spec(item_id, spec_create)
    return spec


@router.put('/{product_id}/items/{item_id}/specs/{spec_id}', summary='修改商品规格')
async def update_item_spec(
    _: dict = Depends(get_product_by_id),
    __: Item = Depends(get_item_by_id),
    current_spec: ItemSpec = Depends(get_item_spec_by_id),
    spec_update: ItemSpecUpdate = Body(...),
    product_repo: ProductRepository = Depends(),
):
    """修改sku规格"""
    spec_id = current_spec.id

    spec = await product_repo.update_item_spec(spec_id, spec_update)
    return spec


@router.delete('/{product_id}/items/{item_id}/specs/{spec_id}', summary='删除商品规格')
async def delete_item_spec(
    _: dict = Depends(get_product_by_id),
    __: Item = Depends(get_item_by_id),
    current_spec: ItemSpec = Depends(get_item_spec_by_id),
    product_repo: ProductRepository = Depends(),
):
    """删除sku规格"""
    spec_id = current_spec.id

    await product_repo.delete_item_spec(spec_id)
    return dict()
