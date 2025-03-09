from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.users.auth import UserDep

router = APIRouter(tags=["page_main"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def get_index_page(
        request: Request,
        user: UserDep = None
):
    is_authenticated = user is not None  # Проверяем, авторизован ли пользователь
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "is_authenticated": is_authenticated},
    )