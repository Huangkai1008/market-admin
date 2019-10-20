from tortoise import fields
from tortoise.models import Model

from app.db.base import ModelTimeMixin

__all__ = ['Brand']


class Brand(Model, ModelTimeMixin):
    """商品品牌"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64, description='品牌名称')
    logo = fields.CharField(null=True, max_length=255, description='品牌logo')
