# from sqlalchemy import Column, Integer, String, ForeignKey
# from db.base import Base
#
# class Item(Base):
#
#     __tablename__ = "items"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)
#
#     owner_id = Column(Integer, ForeignKey("users.id"))

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)  # оригинальная ссылка
    link_id = Column(String(50), unique=True, index=True, nullable=False)  # для редиректа
    owner_user_id = Column(Integer, nullable=True)
    created_at = Column(String, server_default=func.now())
