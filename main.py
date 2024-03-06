from fastapi import FastAPI

from core.config import settings
from db.session import engine
from db import Base


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    create_tables()
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.VERSION}"}
