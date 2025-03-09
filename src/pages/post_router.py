from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.posts.router import get_all_posts


router = APIRouter(prefix="/posts", tags=["page_posts"])
templates = Jinja2Templates(directory="src/templates")


@router.get("")
async def get_post_page(
        request: Request,
        posts=Depends(get_all_posts),
):
    return templates.TemplateResponse(
        name="posts/posts.html",
        context={"request": request, "posts": posts},
    )
