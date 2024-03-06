from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from db import Base


class Tag(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)


class ProjectTag(Base):
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
