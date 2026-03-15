# from pydantic import BaseModel
#
#
# class ItemBase(BaseModel):
#     name: str
#     description: str | None = None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class ItemUpdate(ItemBase):
#     pass
#
#
# class Item(ItemBase):
#     id: int
#     link_id: str  # добавлено для фронта
#
#     class Config:
#         from_attributes = True

from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: str

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    link_id: str
    owner_user_id: Optional[int]

    class Config:
        orm_mode = True
