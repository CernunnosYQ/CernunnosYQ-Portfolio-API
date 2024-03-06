from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from db import Base


class Blogpost(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    banner = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    project = relationship("Project", uselist=False, back_populates="blogpost")
    is_active = Column(Boolean, default=False)
