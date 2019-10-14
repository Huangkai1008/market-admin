from tortoise import fields
from tortoise.models import Model

from app.db.base import ModelTimeMixin


__all__ = ['Store']


class Store(Model, ModelTimeMixin):
    """店铺"""

    id = fields.IntField(pk=True)
    name = fields.CharField(unique=True, max_length=64)  # 店铺名称
    desc = fields.CharField(null=True, max_length=255)  # 店铺简介
