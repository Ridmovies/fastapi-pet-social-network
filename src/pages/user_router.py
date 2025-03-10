from fastapi import APIRouter, Request

from src.templates import templates
from src.users.auth import UserDep

router = APIRouter(prefix="/users", tags=["page_users"])



# @router.get("")
# async def get_index_page(
#         request: Request,
#         user: UserDep,
# ):
#     return templates.TemplateResponse(
#         name="users/index.html",
#         context={"request": request, "user": user},
#     )


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
