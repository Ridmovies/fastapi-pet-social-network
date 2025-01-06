from fastapi import FastAPI

from src.post_app.router import router as post_router
from src.dev_app.router import router as dev_router

app = FastAPI()
app.include_router(post_router)
app.include_router(dev_router)

