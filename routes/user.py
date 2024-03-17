from fastapi import APIRouter, Depends, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db.models.user import (
    create_user,
    delete_user_by_id,
    retrieve_user_by_username,
    update_user_password,
    User,
)
from db.session import get_db
from routes.auth import get_current_user
from schemas import Message, UserCreate, UserShow, UserPasswordUpdate

user_router = APIRouter()


@user_router.post(
    "/create/user", status_code=status.HTTP_201_CREATED, response_model=UserShow
)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.
    """

    if retrieve_user_by_username(user.username, db):
        raise HTTPException(
            detail=f"Username {user.username} is already in use.",
            status_code=status.HTTP_409_CONFLICT,
        )

    user = create_user(user, db)
    return UserShow(**user.__dict__)


@user_router.get("/get/user/{username}", response_model=UserShow)
def read_user_information(username: str, db: Session = Depends(get_db)):
    """
    Retrieve user info by its username
    """

    user = retrieve_user_by_username(username, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserShow(**user.__dict__)


@user_router.put(
    "/update/password/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def update_password(
    id: int,
    pwd_data: UserPasswordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing user's password.
    """

    result = update_user_password(
        user_id=id, pwd_data=pwd_data, db=db, current_user=current_user
    )

    if result.get("success"):
        return Message(message="Password updated successfully")
    else:
        raise HTTPException(**result)


@user_router.delete("/delete/user/{id}")
async def delete_user(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a specific user account. Only available to the owner of the account or admin users.
    """

    result = delete_user_by_id(user_id=id, current_user=current_user, db=db)

    if result.get("success"):
        return Message(message="User removed successfully")
    else:
        raise HTTPException(**result)
