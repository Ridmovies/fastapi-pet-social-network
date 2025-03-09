from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(tags=["page_main"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/")
async def get_index_page(
        request: Request
):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )