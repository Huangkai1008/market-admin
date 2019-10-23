from typing import List

from pydantic import Schema, BaseModel


from app.models.base import OrmModel


class StoreRead(OrmModel):
    """商铺-查询"""

    id: int = Schema(..., title='ID')
    name: str = Schema(..., title='店铺名称')
    desc: str = Schema(None, title='店铺简介')


class StoreList(OrmModel):
    """商铺-列表"""

    stores: List[StoreRead]
    total: int


class StoreCreate(BaseModel):
    """商铺-创建"""

    name: str = Schema(..., max_length=64, title='店铺名称')
    desc: str = Schema(None, max_length=255, title='店铺简介')
