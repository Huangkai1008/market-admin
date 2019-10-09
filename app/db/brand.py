import json

from tortoise import fields
from tortoise.models import Model

from app import utils

__all__ = ['Brand']


class Brand(Model):
    """商品品牌"""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)  # 品牌名称
    cat_ids = fields.JSONField(
        encoder=utils.ExtendedEncoder, decoder=json.decoder
    )  # 品牌涵盖的分类ids
    logo = fields.CharField(max_length=255)  # 品牌logo
