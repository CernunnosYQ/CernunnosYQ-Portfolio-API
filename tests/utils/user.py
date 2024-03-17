from sqlalchemy.orm import Session

from db.models.user import create_user
from core.jwt_utils import create_access_token
from schemas import UserCreate

DEFAULT_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "Password123!",
    "password2": "Password123!",
}


def create_custom_test_user(user_data: dict, db: Session):
    """
    Creates a test user in the database and returs its ID and authentication token.
    """

    user = create_user(user=UserCreate(**user_data), db=db)

    access_token = create_access_token(data={"sub": user.username})

    return user, access_token


def create_default_test_user(db: Session):
    """
    Creates a default test user and returns its ID and authentication token.
    """

    return create_custom_test_user(user=DEFAULT_DATA, db=db)
