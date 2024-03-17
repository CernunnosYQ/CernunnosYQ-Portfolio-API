from fastapi import HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from typing import List, Optional
import re


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    password2: str

    @model_validator(mode="after")
    def validate_password(self):
        pw1 = self.password
        pw2 = self.password2
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise HTTPException(
                detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
            )

        if re.match(pattern, pw1) is None:
            raise HTTPException(
                detail="Password is not secure", status_code=status.HTTP_400_BAD_REQUEST
            )

        return self


class UserShow(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: EmailStr
    full_name: Optional[str] = ""
    avatar: Optional[str] = ""
    about_me: Optional[str] = ""
    socials: Optional[dict] = {}


class UserUpdate(BaseModel):
    full_name: Optional[str] = ""
    avatar: Optional[str] = ""
    about_me: Optional[str] = ""
    socials: Optional[dict] = {}


class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password1: str
    new_passwor2: str

    @model_validator(mode="after")
    def validate_password(self):
        pw1 = self.password1
        pw2 = self.password2
        pattern = (
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        )

        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise HTTPException(
                detail="Passwords do not match", status_code=status.HTTP_400_BAD_REQUEST
            )

        if re.match(pattern, pw1) is None:
            raise HTTPException(
                detail="Password is not secure", status_code=status.HTTP_400_BAD_REQUEST
            )

        return self
