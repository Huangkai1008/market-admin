"""
商品分类
"""
from typing import List

from app.models.base import OrmModel

from pydantic import Schema, BaseModel


class CategoryRead(OrmModel):
    """商品分类-查询"""

    id: int = Schema(..., title='ID')
    parent_id: int = Schema(..., title='父分类, 0表示一级分类')
    cat_name: str = Schema(..., title='分类名')
    cat_level: int = Schema(..., title='分类等级  0 --> 1级;  1 --> 2级')
    cat_keywords: str = Schema(None, max_length=255, title='分类关键词')
    cat_desc: str = Schema(None, title='分类描述')


class CategoryList(OrmModel):
    """商品分类-列表"""

    categories: List[CategoryRead]
    total: int


class CategoryBase(BaseModel):
    """商品分类"""

    cat_keywords: str = Schema(None, max_length=255, title='分类关键词')
    cat_desc: str = Schema(None, title='分类描述')


class CategoryCreate(CategoryBase):
    """商品分类-创建"""

    parent_id: int = Schema(..., ge=0, title='父分类, 0表示一级分类')
    cat_name: str = Schema(..., max_length=64, title='分类名')


class CategoryUpdate(BaseModel):
    """商品分类-修改"""


class CategorySpec(OrmModel):
    """商品分类规格-查询"""

    id: int = Schema(..., title='ID')
    spec_name: str = Schema(..., max_length=64, title='分类规格名称')
    join_select: bool = Schema(..., title='是否可以筛选')
    spec_type: int = Schema(..., title='规格类型  1 销售规格属性 2 展示属性')
    cat_id: int = Schema(..., title='分类id')


class CategorySpecCreate(BaseModel):
    """商品分类规格-创建"""

    spec_name: str = Schema(..., max_length=64, title='分类规格名称')
    join_select: bool = Schema(..., title='是否可以筛选')
    spec_type: int = Schema(..., title='规格类型  1 销售规格属性 2 展示属性')


class CategorySpecUpdate(BaseModel):
    """商品分类规格-修改"""

    join_select: bool = Schema(..., title='是否可以筛选')
