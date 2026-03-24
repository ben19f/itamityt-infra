from pydantic import BaseModel

class LinkBase(BaseModel):
    link_id: str
    original_url: str

class ClickBase(BaseModel):
    link_id: str
    ip: str
    user_agent: str
