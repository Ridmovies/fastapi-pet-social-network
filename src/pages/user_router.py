from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.posts.router import get_all_posts


router = APIRouter(prefix="/users", tags=["page_users"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/login")
async def get_login_page(
        request: Request
):
    return templates.TemplateResponse(
        name="login.html",
        context={"request": request},
    )
