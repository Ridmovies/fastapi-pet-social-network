from fastapi import FastAPI
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from src.admin_app.views import PostAdmin
from src.database import engine
from src.post_app.router import router as post_router
from src.dev_app.router import router as dev_router
from src.auth_app.router import router as auth_router
from src.task_app.router import router as task_router
from src.pages.task_router import router as page_task_router


version = "v1"

description = """
A REST API for a Social Network.

This REST API is able to;
- Create Read Update And delete Posts
    """

version_prefix =f"/api/{version}"


app = FastAPI(
    title="Pet Social Network",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Evgeniy Reshetov",
        "url": "https://github.com/Ridmovies",
    })
app.mount("/static", StaticFiles(directory="src/static"), name="static")
admin = Admin(app, engine)
admin.add_view(PostAdmin)

app.include_router(post_router, prefix=version_prefix)
app.include_router(dev_router, prefix=version_prefix)
app.include_router(auth_router, prefix=version_prefix)
app.include_router(task_router, prefix=version_prefix)
app.include_router(page_task_router)

