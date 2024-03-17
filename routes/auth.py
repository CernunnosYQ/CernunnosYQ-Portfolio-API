from email_validator import validate_email, EmailNotValidError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from core.hashing import Hasher
from core.jwt_utils import create_access_token, validate_access_token
from db.models.user import retrieve_user_by_email, retrieve_user_by_username
from db.session import get_db

auth_router = APIRouter()


def authenticate_user(username: str, password: str, db: Session):
    try:
        _ = validate_email(username)
        user = retrieve_user_by_email(email=username, db=db)
    except EmailNotValidError:
        user = retrieve_user_by_username(username=username, db=db)

        if not user or not Hasher.verify_password(password, user.password):
            return False
        return user


@auth_router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in a user
    """

    user = authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Get current logged-in user
    """

    validation = validate_access_token(token)
    if not validation.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=validation.get("detail")
        )
    user = retrieve_user_by_username(
        username=validation.get("payload").get("sub"), db=db
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not validate credentials",
        )
    return user
