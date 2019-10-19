from tortoise import fields
from tortoise.models import Model


__all__ = ['Brand']


class Brand(Model):
    """商品品牌"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)  # 品牌名称
    logo = fields.CharField(null=True, max_length=255)  # 品牌logo
