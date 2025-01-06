from fastapi import FastAPI
from sqladmin import Admin

from src.admin_app.views import PostAdmin
from src.database import engine
from src.post_app.router import router as post_router
from src.dev_app.router import router as dev_router
from src.pages.router import router as page_router


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
admin = Admin(app, engine)
admin.add_view(PostAdmin)

app.include_router(post_router, prefix=version_prefix)
app.include_router(dev_router, prefix=version_prefix)
app.include_router(page_router, prefix="/page")

