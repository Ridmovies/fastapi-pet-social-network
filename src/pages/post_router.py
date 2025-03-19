from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.auth2.jwt_utils import UserDep
from src.posts.router import get_all_posts, get_post_details

router = APIRouter(prefix="/posts", tags=["page_posts"])
templates = Jinja2Templates(directory="src/templates")


@router.get("")
async def get_post_page(
    request: Request,
    user: UserDep,
    posts=Depends(get_all_posts),
):
    return templates.TemplateResponse(
        name="posts/posts.html",
        context={"request": request, "posts": posts, "user": user},
    )


@router.get("/{post_id}/details")
async def get_post_details_page(
    request: Request,
    user: UserDep,
    post=Depends(get_post_details),
):
    return templates.TemplateResponse(
        name="posts/post_detail.html",
        context={"request": request, "post": post, "user": user},
    )
