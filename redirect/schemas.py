from pydantic import BaseModel

class LinkCreate(BaseModel):
    link_id: str
    original_url: str
    owner_user_id: int | None = None

class LinkOut(BaseModel):
    link_id: str
    original_url: str
    owner_user_id: int | None = None

    class Config:
        orm_mode = True