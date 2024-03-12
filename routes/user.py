from fastapi import APIRouter, Depends, HTTPException, status
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import Session

from db.models.user import create_user, retrieve_user_by_username
from db.session import get_db
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


# @user_router.put(
#     "/update/password/{id}",
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=Message
# )
# def  update_user_password(
#     id: int, password: UserPasswordUpdate, db: Session = Depends(get_db)
# ):
#     """
#     Update an existing user's password.
#     """

#     pass


# @user_router.delete("/remove/{id}")
# async def remove_user(
#     id: int,
#     current_user: User = Depends(is_self_or_admin),
#     db: Session = Depends(get_db),
# ):
#     """
#     Delete a specific user account. Only available to the owner of the account or admin users.
#     """

#     pass
