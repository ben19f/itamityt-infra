from sqlalchemy import Column, Integer, String, ForeignKey
from db.base import Base

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

