from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from src.post_app.router import get_all_posts

router = APIRouter()


templates = Jinja2Templates(directory="src/templates")


@router.get("/posts")
async def get_posts_page(
    request: Request,
    posts=Depends(get_all_posts),
):
    return templates.TemplateResponse(
        name="posts.html",
        context={"request": request, "posts": posts},
    )
