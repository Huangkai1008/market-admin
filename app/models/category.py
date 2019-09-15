from tortoise import fields
from tortoise.models import Model

__all__ = ['ProductCategory']


class ProductCategory(Model):
    """商品分类"""

    id = fields.IntField(pk=True)
    parent_id = fields.IntField(index=True, default=0)  # 父分类, 0表示一级分类
    cat_name = fields.CharField(max_length=64, unique=True)  # 分类名
    cat_level = fields.SmallIntField(index=True)  # 分类等级  0 --> 1级;  1 --> 2级
    cat_keywords = fields.CharField(max_length=255)  # 分类关键词
    cat_desc = fields.TextField()  # 分类描述
