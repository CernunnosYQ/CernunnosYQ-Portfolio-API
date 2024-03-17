from jwt import encode, exceptions, decode
from typing import Optional
from datetime import datetime, timedelta, UTC

from core.config import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.TOKEN_EXPIRE_MINS)

    token = encode(
        payload={**data, "exp": expire},
        key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def validate_access_token(token: bytes) -> dict:
    try:
        decoded_token = decode(
            token, key=settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )

        return {"success": True, "payload": decoded_token}
    except exceptions.DecodeError:
        detail = "Invalid token."
    except exceptions.ExpiredSignatureError:
        detail = "Token has expired"

    return {"success": False, "detail": detail}
