from typing import List

from pydantic import Schema, BaseModel


from app.models.base import OrmModel


class BrandRead(OrmModel):
    """商品品牌-查询"""

    id: int = Schema(..., title='ID')
    name: int = Schema(..., title='品牌名称')


class BrandList(OrmModel):
    """商品品牌-列表"""

    brands: List[BrandRead]
    total: int


class BrandCreate(BaseModel):
    """商品品牌-创建"""

    name: int = Schema(..., title='品牌名称')
