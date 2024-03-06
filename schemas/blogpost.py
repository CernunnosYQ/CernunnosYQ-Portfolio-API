from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional


class BlogpostCreate(BaseModel):
    title: str
    slug: str
    banner: Optional[str] = ""
    content: Optional[str] = ""
    is_active: Optional[bool] = True

    @model_validator(mode="before")
    @classmethod
    def check_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class BlogpostShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    banner: str
    content: str
    created_at: datetime
    author: str


class BlogpostUpdate(BlogpostCreate):
    pass
