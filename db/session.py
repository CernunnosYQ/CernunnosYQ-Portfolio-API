from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from core.config import settings


DB_URL = settings.DB_URL
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
