from fastapi import APIRouter, Request

from src.templates import templates
from src.users.auth import UserDep

router = APIRouter(tags=["page_main"])


@router.get("/")
async def get_index_page(
        request: Request,
        user: UserDep = None
):
    is_authenticated = user is not None  # Проверяем, авторизован ли пользователь
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "user": user}
    )