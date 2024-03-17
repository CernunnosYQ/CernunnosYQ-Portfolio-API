from fastapi import status
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
from schemas import UserCreate, UserUpdate, UserPasswordUpdate
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


def retrieve_user_by_email(email: str, db: Session) -> User:
    user = db.query(User).filter(User.email == email).first()

    return user


def update_user_password(
    user_id: int, pwd_data: UserPasswordUpdate, current_user: User, db: Session
):
    user_in_db = db.query(User).filter(User.id == user_id).one_or_none()
    if not user_in_db:
        return {"status_code": status.HTTP_404_NOT_FOUND, "detail": "User not found"}
    if not current_user.is_superuser and current_user != user_in_db:
        return {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "Only the owner or an admin can change the password",
        }
    if not Hasher.verify_password(pwd_data.old_password, user_in_db.password):
        return {"status_code": status.HTTP_401_UNAUTHORIZED, "detail": "Wrong password"}
    user_in_db.password = Hasher.hash_password(pwd_data.new_password)
    db.commit()

    return {"success": True}


def delete_user_by_id(user_id: int, current_user: User, db: Session):
    user_in_db = db.query(User).filter(User.id == user_id).one_or_none()
    if not user_in_db:
        return {"status_code": status.HTTP_404_NOT_FOUND, "detail": "User not found"}
    if not current_user.is_superuser and current_user != user_in_db:
        return {
            "status_code": status.HTTP_403_FORBIDDEN,
            "detail": "You do not have permission to perform this action.",
        }
    db.delete(user_in_db)
    db.commit()
    return {"success": True}
