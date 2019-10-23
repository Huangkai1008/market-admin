"""
商品
"""
from typing import List

from pydantic import Schema

from app.models.base import OrmModel


class ProductRead(OrmModel):
    """
    商品-查询
    """

    id: int = Schema(..., title='ID')
    product_name: str = Schema(..., title='商品')
    product_sn: str = Schema(..., title='商品货号')
    sub_title: str = Schema(None, title='副标题')
    cat_id: str = Schema(..., title='商品分类id')
    brand_id: str = Schema(..., title='品牌id')
    brand_name: str = Schema(..., title='品牌名')
    store_id: str = Schema(..., title='商铺id')
    store_name: str = Schema(..., title='商铺名')
    unit: str = Schema(..., title='单位(件/台...)')
    published: bool = Schema(..., title='上架状态')


class ProductList(OrmModel):
    """
    商品-列表
    """

    products: List[ProductRead]
    total: int


class ProductCreate(OrmModel):
    """
    商品-创建
    """

    product_name: str = Schema(..., max_length=64, title='商品')
    product_sn: str = Schema(..., max_length=24, title='商品货号')
    sub_title: str = Schema(None, max_length=128, title='副标题')
    cat_id: int = Schema(..., ge=1, title='商品分类id')
    brand_id: int = Schema(..., ge=1, title='品牌id')
    store_id: int = Schema(..., ge=1, title='商铺id')
    unit: str = Schema(..., max_length=32, title='单位(件/台...)')
    published: bool = Schema(..., title='上架状态')
