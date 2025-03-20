from fastapi import APIRouter, Request, Depends

from src.auth2.jwt_utils import UserDep
from src.templates import templates
from src.users.router import get_all_users, get_user_by_id_with_followers

router = APIRouter(prefix="/users", tags=["page_users"])


@router.get("")
async def get_users_page(
        request: Request,
        user: UserDep,
        users=Depends(get_all_users)):
    return templates.TemplateResponse(
        name="users/users_list.html",
        context={"request": request, "users": users, "user": user},
    )


@router.get("/me")
async def get_user_page(
    request: Request,
    user: UserDep,
):
    return templates.TemplateResponse(
        name="users/me.html",
        context={"request": request, "user": user},
    )


@router.get("/login")
async def get_login_page(request: Request):
    return templates.TemplateResponse(
        name="users/login.html",
        context={"request": request},
    )


@router.get("/register")
async def get_register_page(request: Request):
    return templates.TemplateResponse(
        name="users/register.html",
        context={"request": request},
    )


@router.get("/{user_id}")
async def get_user_page(
    request: Request,
    user: UserDep,
    follow_user=Depends(get_user_by_id_with_followers),
):
    return templates.TemplateResponse(
        name="users/user_detail.html",
        context={"request": request, "user": user, "follow_user": follow_user},
    )
