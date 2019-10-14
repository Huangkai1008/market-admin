from app.db.base import ModelTimeMixin

from tortoise import fields
from tortoise.models import Model


__all__ = ['ProductCategory']


class ProductCategory(Model, ModelTimeMixin):
    """商品分类"""

    id = fields.IntField(pk=True)
    parent_id = fields.IntField(index=True, default=0, description='父分类, 0表示一级分类')
    cat_name = fields.CharField(max_length=64, unique=True, description='分类名')
    cat_level = fields.SmallIntField(
        index=True, description='分类等级  0 --> 1级;  1 --> 2级'
    )
    cat_keywords = fields.CharField(max_length=255, null=True, description='分类关键词')
    cat_icon = fields.CharField(max_length=255, null=True, description='分类图标')  # 分类图标
    cat_desc = fields.TextField(null=True, description='分类描述')

    class Meta:
        table = 'product_category'
