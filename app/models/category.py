"""
商品分类
"""
from app.models.base import OrmModel


from pydantic import Schema
from pydantic.dataclasses import dataclass


class CategoryRead(OrmModel):
    """商品分类-查询"""

    id: int
    parent_id: int
    cat_name: str
    cat_level: int
    cat_keywords: str = None
    cat_desc: str = None


@dataclass
class CategoryBase:
    parent_id: int = Schema(..., ge=0)
    cat_name: str = Schema(..., max_length=64)


@dataclass
class CategoryCreate(CategoryBase):
    """商品分类-创建"""

    cat_level: int = Schema(..., ge=0)  # 分类等级  0 --> 1级;  1 --> 2级
    cat_keywords: str = Schema(None, max_length=255)  # 分类关键词
    cat_desc: str = None


class CategorySpec(OrmModel):
    """商品分类规格-查询"""

    id: int
    spec_number: str
    spec_name: str
    join_select = bool
