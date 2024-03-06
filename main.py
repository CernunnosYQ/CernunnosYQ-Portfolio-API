from fastapi import FastAPI

from core.config import settings
from db.session import engine
from db import Base
from routes import api_router


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def include_routers(app: FastAPI) -> None:
    app.include_router(api_router, prefix="/api")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
    create_tables()
    include_routers(app)
    return app


app = create_app()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.VERSION}"}
