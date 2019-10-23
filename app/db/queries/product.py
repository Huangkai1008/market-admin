from typing import Tuple, List

from fastapi.encoders import jsonable_encoder

from app.db.product import Product
from app.db.queries.utils import and_pagination
from app.models.product import ProductCreate


async def get_products(
    page: int, size: int, *, cat_id: int
) -> Tuple[List[Product], int]:
    """获取商品列表"""
    conditions = dict()

    if cat_id is not None:
        conditions['cat_id'] = cat_id

    total = await Product.filter(**conditions).count()

    products = await and_pagination(Product.filter(**conditions), page, size).values(
        'id',
        'product_name',
        'product_sn',
        'sub_title',
        'cat_id',
        'unit',
        'published',
        'brand_id',
        'store_id',
        brand_name='brand__name',
        store_name='store__name',
    )
    return products, total


async def get_product(product_id) -> Product:
    """获取单个商品"""
    products = await Product.get(id=product_id).values(
        'id',
        'product_name',
        'product_sn',
        'sub_title',
        'cat_id',
        'unit',
        'published',
        'brand_id',
        'store_id',
        brand_name='brand__name',
        store_name='store__name',
    )
    return products[0]


async def create_product(product_create: ProductCreate) -> Product:
    """创建商品"""
    product_create_data = jsonable_encoder(product_create)
    product = Product(**product_create_data)
    await product.save()
    product = await get_product(product.id)
    return product
