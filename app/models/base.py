from enum import IntEnum

from pydantic import BaseModel


class OrmModel(BaseModel):
    """添加orm_mode"""

    class Config:
        orm_mode = True


class SpecType(IntEnum):
    """规格类型"""

    sales = 1
    display = 2
