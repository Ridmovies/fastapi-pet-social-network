from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.users.router import read_users_me

router = APIRouter(prefix="/users", tags=["page_users"])
templates = Jinja2Templates(directory="src/templates")


@router.get("")
async def get_index_page(
        request: Request
):
    return templates.TemplateResponse(
        name="users/index.html",
        context={"request": request},
    )


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


@router.get("/register")
async def get_register_page(
        request: Request
):
    return templates.TemplateResponse(
        name="users/register.html",
        context={"request": request},
    )
