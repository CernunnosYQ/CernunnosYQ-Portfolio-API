from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


DB_URL = settings.DB_URL
engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
