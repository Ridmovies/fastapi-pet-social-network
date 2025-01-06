from fastapi import FastAPI
from sqladmin import Admin

from src.admin_app.views import PostAdmin
from src.database import engine
from src.post_app.router import router as post_router
from src.dev_app.router import router as dev_router

app = FastAPI()
admin = Admin(app, engine)
admin.add_view(PostAdmin)

app.include_router(post_router)
app.include_router(dev_router)

