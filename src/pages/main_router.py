from fastapi import APIRouter, Request

from src.auth2.jwt_utils import UserOrGuestDep
from src.templates import templates

router = APIRouter(tags=["page_main"])


@router.get("/")
async def get_index_page(
    request: Request,
    user: UserOrGuestDep,
):
    return templates.TemplateResponse(
        name="index.html", context={"request": request, "user": user}
    )
