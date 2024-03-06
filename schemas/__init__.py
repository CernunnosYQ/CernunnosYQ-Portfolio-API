from .blogpost import BlogpostCreate, BlogpostShow, BlogpostUpdate
from .project import ProjectShow, ProjectCreate, ProjectUpdate
from .user import UserCreate, UserShow, UserUpdate, UserPasswordUpdate

from pydantic import BaseModel


class Message(BaseModel):
    message: str
