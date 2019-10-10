"""
商品分类
"""

from pydantic import Schema
from pydantic.dataclasses import dataclass


@dataclass
class ProductCategoryBase:
    parent_id: int = Schema(0)
    cat_name: str = Schema(..., max_length=64)
    cat_level: int = Schema(...)  # 分类等级  0 --> 1级;  1 --> 2级


@dataclass
class ProductCategory:
    """商品分类"""

    parent_id: int = Schema(0)
    cat_name: str = Schema(..., max_length=64)
    cat_level: int = Schema(...)  # 分类等级  0 --> 1级;  1 --> 2级
    cat_keywords: str = Schema(None, max_length=255)  # 分类关键词
    cat_desc: str = None
