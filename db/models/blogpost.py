from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship, Session, joinedload
from sqlalchemy.sql import func
from fastapi import status

from db import Base
from schemas import BlogpostCreate, BlogpostUpdate


class Blogpost(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    content = Column(Text, nullable=False)
    banner = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="posts")
    created_at = Column(DateTime, default=func.now(), nullable=False)
    project = relationship("Project", uselist=False, back_populates="post")
    is_active = Column(Boolean, default=False)


def check_if_title_exists(title: str, db: Session):
    slug = title.replace(" ", "-").lower()
    post = (
        db.query(Blogpost)
        .filter(Blogpost.slug == slug)
        .options(joinedload(Blogpost.author))
        .first()
    )
    return False if not post else True


def retrieve_post_list(db: Session):
    return (
        db.query(Blogpost)
        .order_by(Blogpost.created_at.desc())
        .options(joinedload(Blogpost.author))
        .all()
    )


def create_new_blogpost(blogpost: BlogpostCreate, db: Session):
    new_blogpost = Blogpost(**blogpost.__dict__, author_id=5)
    db.add(new_blogpost)
    db.commit()
    return retrieve_blogpost_by_slug(new_blogpost.slug, db)


def retrieve_blogpost_by_id(id: int, db: Session):
    return (
        db.query(Blogpost)
        .filter(Blogpost.id == id)
        .options(joinedload(Blogpost.author))
        .first()
    )


def retrieve_blogpost_by_slug(slug: str, db: Session):
    return (
        db.query(Blogpost)
        .filter(Blogpost.slug == slug)
        .options(joinedload(Blogpost.author))
        .one_or_none()
    )


def update_blogpost_with_id(post_id: int, new_data: BlogpostUpdate, db: Session):
    old_post = retrieve_blogpost_by_id(post_id, db)
    if not old_post:
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": f"Post with ID {post_id} does not exists.",
        }

    for key, value in new_data.__dict__.items():
        setattr(old_post, key, value)

    db.commit()
    return retrieve_blogpost_by_id(post_id, db)


def delete_blogpost_by_id(post_id: int, db: Session):
    post_to_be_deleted = db.query(Blogpost).filter(Blogpost.id == post_id)
    if not post_to_be_deleted.one_or_none():
        return {
            "status_code": status.HTTP_404_NOT_FOUND,
            "detail": f"Post with ID {post_id} does not exists.",
        }

    post_to_be_deleted.delete()
    db.commit()
    return {"success": True}
