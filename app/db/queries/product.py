from typing import Tuple, List, Iterable

from fastapi.encoders import jsonable_encoder
from tortoise.transactions import atomic

from app import utils
from app.db.product import Product, Item, ItemSpec
from app.db.queries.utils import and_pagination
from app.models.product import ProductCreate, ProductUpdate, ItemCreate, ItemUpdate


async def get_products(
    page: int, size: int, *, cat_id: int = None
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

    return products[0] if products else None


async def create_product(product_create: ProductCreate) -> Product:
    """创建商品"""
    product_create_data = jsonable_encoder(product_create)
    product = Product(**product_create_data)
    await product.save()
    product = await get_product(product.id)
    return product


async def update_product(product_id: int, product_update: ProductUpdate) -> Product:
    """更新商品"""
    product_update_data = jsonable_encoder(product_update)
    await Product.get(id=product_id).update(**product_update_data)
    product = await get_product(product_id)
    return product


async def get_items(*, page: int = None, size: int = None) -> Tuple[List[Item], int]:
    """获取商品sku列表"""
    conditions = dict()

    total = await Item.filter(**conditions).count()

    items = await Item.filter(**conditions)

    if page and size:
        items = and_pagination(items, page, size)

    return items, total


async def get_item(item_id: int) -> Item:
    """获取商品sku"""
    queryset = await Item.get(id=item_id)
    return queryset


@atomic()
async def bulk_create_sku(
    product_id: int, cat_id: int, item_bulk_create: List[ItemCreate]
):
    """批量创建商品sku"""
    item_bulk_create_data = jsonable_encoder(item_bulk_create)

    snow_flake = utils.Snowflake()

    ids = [snow_flake.generate_id() for _ in range(len(item_bulk_create_data))]

    for index, item_create_data in enumerate(item_bulk_create_data):
        sku_number = ids[index]
        specs = item_create_data.pop('specs')
        item = Item(
            **item_create_data,
            product_id=product_id,
            sku_number=sku_number,
            cat_id=cat_id
        )
        await item.save()
        item_id = item.id
        await ItemSpec.bulk_create(
            [
                ItemSpec(
                    spec_name=spec['spec_name'],
                    spec_type=spec['spec_type'],
                    spec_value=spec['spec_value'],
                    item_id=item_id,
                )
                for spec in specs
            ]
        )


async def update_item(item_id: int, item_update: ItemUpdate) -> Item:
    """更新商品sku"""
    item_update_data = jsonable_encoder(item_update)
    await Item.get(id=item_id).update(**item_update_data)
    item = await get_item(item_id)
    return item


async def get_item_specs(
    *, item_id: int = None, item_ids: Iterable = None, item_id_sort: bool = None
) -> List[ItemSpec]:
    """获取商品sku规格属性"""
    conditions = dict()
    orderings = list()

    if item_id:
        conditions['item_id'] = item_id
    if item_ids is not None:
        conditions['item_id__in'] = item_ids

    if item_id_sort is not None:
        ordering = 'item_id' if item_id_sort else '-item_id'
        orderings.append(ordering)
    items = await ItemSpec.filter(**conditions).order_by(*orderings).all()
    return items
