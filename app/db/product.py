from tortoise import fields
from tortoise.models import Model

from app.db.base import ModelTimeMixin


__all__ = ['Product', 'Item']


class Product(Model, ModelTimeMixin):
    """商品(SPU)"""

    id = fields.IntField(pk=True)
    product_name = fields.CharField(max_length=64, index=True, description='商品名称')
    product_sn = fields.CharField(max_length=24, unique=True, description='商品货号')
    sub_title = fields.CharField(max_length=128, null=True, description='副标题')
    cat_id = fields.IntField(index=True, description='商品分类id')
    brand_id = fields.IntField(index=True, description='品牌id')
    store_id = fields.IntField(index=True, description='商铺id')
    unit = fields.CharField(max_length=32, description='单位(件/台...)')
    published = fields.BooleanField(unique=True, description='上架状态')


class Item(Model, ModelTimeMixin):
    """商品单品(SKU)"""

    id = fields.IntField(pk=True)
    sku_number = fields.CharField(max_length=36, unique=True, description='sku编号')
    product_id = fields.IntField(index=True, description='商品id')
    price = fields.FloatField(description='价格')
    stock = fields.IntField(description='库存')
    sales = fields.IntField(description='销量')
