from sqlalchemy.orm import Session
import re, random, string

from db.models.user import create_user
from core.jwt_utils import create_access_token
from schemas import UserCreate


def create_custom_test_user(user_data: dict, db: Session):
    """
    Creates a test user in the database and returs its ID and authentication token.
    """

    user = create_user(user=UserCreate(**user_data), db=db)

    access_token = create_access_token(data={"sub": user.username})

    return user, access_token


def create_random_test_user(db: Session):
    """
    Creates a random test user and returns its ID, password and authentication token.
    """

    username = generate_random_username()
    plain_password = generate_random_password(12)

    random_user_data = {
        "username": username,
        "email": f"{username.lower()}@example.com",
        "password": plain_password,
        "password2": plain_password,
    }

    user = create_user(user=UserCreate(**random_user_data), db=db)

    access_token = create_access_token(data={"sub": user.username})

    return user, plain_password, access_token


def generate_random_username(length: int = 10) -> str:
    random_string = "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )
    return random_string


def generate_random_password(length: int = 10) -> str:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    while True:
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits + "@$!%*?&", k=length)
        )
        if re.match(pattern=pattern, string=random_string):
            return random_string
