from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.models.blogpost import (
    retrieve_post_list,
    retrieve_blogpost_by_id,
    retrieve_blogpost_by_slug,
    check_if_title_exists,
    create_new_blogpost,
    update_blogpost_with_id,
    delete_blogpost_by_id,
)
from db.session import get_db
from schemas import BlogpostShow, BlogpostCreate, BlogpostUpdate, Message

blog_router = APIRouter()


@blog_router.get("/get/post/all", response_model=List[BlogpostShow])
def get_all_posts(db: Session = Depends(get_db)):
    """
    Get all blog posts
    """

    return [BlogpostShow(**post.__dict__) for post in retrieve_post_list(db=db)]


@blog_router.get("/get/post/by-id/{post_id}", response_model=BlogpostShow)
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    """
    Get a single blog post by its id
    """

    post = retrieve_blogpost_by_id(id=post_id, db=db)
    return BlogpostShow(**post.__dict__)


@blog_router.get("/get/post/by-slug/{post_slug}", response_model=BlogpostShow)
def get_post_by_slug(post_slug: str, db: Session = Depends(get_db)):
    """
    Get a single blog post by its slug
    """

    post = retrieve_blogpost_by_slug(slug=post_slug, db=db)
    return BlogpostShow(**post.__dict__)


@blog_router.post("/create/post")
def create_new_post(post: BlogpostCreate, db: Session = Depends(get_db)):
    """
    Creates a new blog post
    """

    title_exists = check_if_title_exists(title=post.title, db=db)

    if title_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Title already exists."
        )

    new_post = create_new_blogpost(blogpost=post, db=db)
    return BlogpostShow(**new_post.__dict__)


@blog_router.put("/update/post/{post_id}")
def update_existing_post(
    post_id: int, new_data: BlogpostUpdate, db: Session = Depends(get_db)
):
    """
    Updates an existing blog post
    """

    updated_post = update_blogpost_with_id(post_id=post_id, new_data=new_data, db=db)
    if isinstance(updated_post, dict):
        raise HTTPException(**updated_post)

    return BlogpostShow(**updated_post.__dict__)


@blog_router.delete("/delete/post/{post_id}", response_model=Message)
def delete_existing_post(post_id: int, db: Session = Depends(get_db)):
    """
    Deletes a specific blog post by ID
    """

    result = delete_blogpost_by_id(post_id=post_id, db=db)

    if result.get("success"):
        return {"message": "Blogpost deleted successfully"}
    else:
        raise HTTPException(**result)
