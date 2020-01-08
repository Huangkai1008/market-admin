from fastapi import Path, HTTPException, Depends
from starlette.status import HTTP_404_NOT_FOUND

from app.db.repositories.product import ProductRepository


async def get_product_by_id(
    product_id: int = Path(..., ge=1, description='商品id'),
    product_repo: ProductRepository = Depends(),
):
    product = await product_repo.get_product(product_id)
    if not product:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return product


async def get_item_by_id(
    item_id: int = Path(..., ge=1, description='sku id'),
    product_repo: ProductRepository = Depends(),
):
    item = await product_repo.get_item(item_id)
    if not item:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return item


async def get_item_spec_by_id(
    spec_id: int = Path(..., ge=1, description='规格id'),
    product_repo: ProductRepository = Depends(),
):
    spec = await product_repo.get_item_spec(spec_id=spec_id)
    if not spec:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    return spec
