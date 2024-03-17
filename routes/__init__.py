from fastapi import APIRouter

from .user import user_router
from .blogpost import blog_router
from .auth import auth_router


api_router = APIRouter()
api_router.include_router(user_router, prefix="", tags=["users"])
api_router.include_router(blog_router, prefix="", tags=["blogposts"])
api_router.include_router(auth_router, prefix="", tags=["authentication"])
