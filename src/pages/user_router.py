from fastapi import APIRouter, Request, Depends

from src.templates import templates
from src.users.auth import UserDep
from src.users.router import get_all_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["page_users"])


@router.get("")
async def get_users_page(
        request: Request,
        users=Depends(get_all_users)
):
    return templates.TemplateResponse(
        name="users/users_list.html",
        context={"request": request, "users": users},
    )


@router.get("/{user_id}")
async def get_user_page(
        request: Request,
        user=Depends(get_user_by_id),
):
    return templates.TemplateResponse(
        name="users/user_detail.html",
        context={"request": request, "user": user},
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
        user: UserDep,
):
    return templates.TemplateResponse(
        name="users/profile.html",
        context={"request": request, "user": user},
    )


@router.get("/register")
async def get_register_page(
        request: Request
):
    return templates.TemplateResponse(
        name="users/register.html",
        context={"request": request},
    )
