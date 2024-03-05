from fastapi import FastAPI

from core.config import settings


app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} v{settings.VERSION}"}
