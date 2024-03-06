from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from db import Base


class Project(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    banner = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="projects")
    post_id = Column(Integer, ForeignKey("blogposts.id"))
    post = relationship("Blogpost", back_populates="project")
    last_update = Column(DateTime, default=func.now(), nullable=False)
    live_view = Column(String)  # URL to the live view of this project
    repo = Column(String)  # URL of the project's GitHub repository
    container = Column(String)  # Docker image name for this project
    stack = relationship(
        "Tag", secondary="projecttags"
    )  # Technologies used in this project
    is_active = Column(Boolean, default=False)
