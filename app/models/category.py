"""
商品分类
"""
from typing import List

from app.models.base import OrmModel


from pydantic import Schema, BaseModel


class CategoryRead(OrmModel):
    """商品分类-查询"""

    id: int
    parent_id: int
    cat_name: str
    cat_level: int
    cat_keywords: str = None
    cat_desc: str = None


class CategoryList(OrmModel):
    """商品分类-列表"""

    categories: List[CategoryRead]
    total: int


class CategoryBase(BaseModel):
    """商品分类"""

    cat_keywords: str = Schema(None, max_length=255)  # 分类关键词
    cat_desc: str = None


class CategoryCreate(CategoryBase):
    """商品分类-创建"""

    parent_id: int = Schema(..., ge=0)
    cat_name: str = Schema(..., max_length=64)
    cat_level: int = Schema(..., ge=0)  # 分类等级  0 --> 1级;  1 --> 2级


class CategoryUpdate(BaseModel):
    """商品分类-修改"""


class CategorySpec(OrmModel):
    """商品分类规格-查询"""

    id: int
    spec_number: str
    spec_name: str
    join_select = bool
