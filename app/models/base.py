from pydantic import BaseModel


class OrmModel(BaseModel):
    """添加orm_mode"""

    class Config:
        orm_mode = True
