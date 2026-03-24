from sqlalchemy import Column, String, Integer, Text, TIMESTAMP, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(String(50), unique=True, index=True, nullable=False)
    original_url = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    owner_user_id = Column(Integer, nullable=True)  # если нужно привязать к пользователю

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(String(50), ForeignKey("links.link_id"))
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ip = Column(String(50))
    user_agent = Column(Text)
