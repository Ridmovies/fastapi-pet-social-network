from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.users.router import read_users_me

router = APIRouter(prefix="/users", tags=["page_users"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/login")
async def get_login_page(
        request: Request
):
    return templates.TemplateResponse(
        name="users/login.html",
        context={"request": request},
    )

@router.get("/profile")
async def get_profile_page(
        request: Request,
        profile=Depends(read_users_me),
):
    return templates.TemplateResponse(
        name="users/profile.html",
        context={"request": request, "profile": profile},
    )
