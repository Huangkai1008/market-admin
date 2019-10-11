"""
商品分类
"""

from pydantic import Schema, BaseModel
from pydantic.dataclasses import dataclass


class CategoryRead(BaseModel):
    """商品分类-查询"""

    id: int
    parent_id: int
    cat_name: str
    cat_level: int
    cat_keywords: str = None
    cat_desc: str = None

    class Config:
        orm_mode = True


@dataclass
class CategoryBase:
    parent_id: int = Schema(0)
    cat_name: str = Schema(..., max_length=64)


@dataclass
class CategoryCreate(CategoryBase):
    """商品分类-创建"""

    cat_level: int = Schema(...)  # 分类等级  0 --> 1级;  1 --> 2级
    cat_keywords: str = Schema(None, max_length=255)  # 分类关键词
    cat_desc: str = None
