from tortoise import fields
from tortoise.models import Model

from app.db.base import ModelTimeMixin


__all__ = ['Product', 'Item', 'ItemSpec', 'ItemAttr']


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
    introduction = fields.TextField(description='商品介绍')


class ItemSpec(Model, ModelTimeMixin):
    """
    商品规格信息
    继承分类规格信息 属于销售信息 不可在分类规格信息上扩展
    """

    item_id = fields.IntField()
    spec_number = fields.CharField(max_length=32, description='规格编号')  # color
    spec_name = fields.CharField(max_length=64, description='规格名称')  # 颜色
    spec_value = fields.CharField(max_length=128, description='规格值')  # 红

    class Meta:
        table = 'item_spec'
        pk_field = {'item_id', 'spec_number'}
        unique_together = [('item_id', 'spec_name')]


class ItemAttr(Model, ModelTimeMixin):
    """
    商品属性信息
    继承分类属性信息 参与筛选与展示 可在分类属性信息上扩展
    """

    item_id = fields.IntField()
    attr_name = fields.CharField(max_length=64, description='分类属性名称')  # 内存容量 ...
    attr_value = fields.CharField(max_length=128, description='分类属性值')  # 16G ...

    class Meta:
        table = 'item_attr'
        pk_field = {'item_id', 'attr_name'}
