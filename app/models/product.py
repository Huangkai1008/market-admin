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
    cat_id: int = Schema(..., title='商品分类id')
    brand_id: int = Schema(..., title='品牌id')
    brand_name: str = Schema(..., title='品牌名')
    store_id: int = Schema(..., title='商铺id')
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

    product_name: str = Schema(..., max_length=64, title='商品名')
    product_sn: str = Schema(..., max_length=24, title='商品货号')
    sub_title: str = Schema(None, max_length=128, title='副标题')
    cat_id: int = Schema(..., ge=1, title='商品分类id')
    brand_id: int = Schema(..., ge=1, title='品牌id')
    store_id: int = Schema(..., ge=1, title='商铺id')
    unit: str = Schema(..., max_length=32, title='单位(件/台...)')
    published: bool = Schema(..., title='上架状态')


class ProductUpdate(OrmModel):
    """
    商品-修改
    """

    sub_title: str = Schema(None, max_length=128, title='副标题')
    unit: str = Schema(..., max_length=32, title='单位(件/台...)')
    published: bool = Schema(..., title='上架状态')


class ItemSpec(OrmModel):
    spec_name: str = Schema(..., max_length=64, title='规格名称')
    spec_value: str = Schema(..., title='规格值')
    spec_type: int = Schema(..., title='规格类型  1 销售规格属性 2 展示属性')


class ItemCreate(OrmModel):
    """
    商品sku-新增
    """

    price: float = Schema(..., ge=0, title='价格')
    stock: int = Schema(..., ge=0, title='库存')
    sales: int = Schema(..., ge=0, title='销量')
    introduction: str = Schema(..., title='商品sku介绍')
    specs: List[ItemSpec] = Schema(..., title='规格信息')
