from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from pydantic.functional_validators import BeforeValidator
from typing import Optional, List
from typing_extensions import Annotated


class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = ""
    banner: Optional[str] = ""
    post: Optional[str] = ""
    repo: Optional[str] = ""
    container: Optional[str] = ""
    live_view: Optional[str] = ""
    stack: List[str] = []
    is_active: Optional[bool] = True

    @model_validator(mode="before")
    @classmethod
    def check_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


TagType = Annotated[str, BeforeValidator(lambda tag: tag.name)]


class ProjectShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    slug: str
    banner: str
    description: str
    created_at: datetime
    author: str
    post: str = ""
    repo: str = ""
    container: str = ""
    live_view: str = ""
    stack: List[TagType]


class ProjectUpdate(ProjectCreate):
    pass
