from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func

from core.hashing import Hasher
from schemas import UserCreate, UserUpdate
from db import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    full_name = Column(String)
    avatar = Column(String)  # URL to avatar img
    about_me = Column(Text)
    socials = Column(JSON)
    date_joined = Column(DateTime, default=func.now())
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    posts = relationship("Blogpost", back_populates="author")
    projects = relationship("Project", back_populates="author")


def create_user(user: UserCreate, db: Session) -> User:
    user = User(
        username=user.username,
        password=Hasher.hash_password(user.password),
        email=user.email,
    )
    db.add(user)
    db.commit()

    return retrieve_user_by_username(username=user.username, db=db)


def retrieve_user_by_username(username: str, db: Session) -> User:
    user = db.query(User).filter(User.username == username).first()

    return user
