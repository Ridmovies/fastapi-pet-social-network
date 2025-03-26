from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates

from src.auth2.jwt_utils import UserDep
from src.posts.router import get_all_posts, get_post_details, get_my_feed

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


@router.get("/create")
async def get_post_page(
    request: Request,
    user: UserDep,
):
    return templates.TemplateResponse(
        name="posts/create_post.html",
        context={"request": request, "user": user},
    )

@router.get("/feed")
async def get_my_feed_page(
    request: Request,
    user: UserDep,
    posts=Depends(get_my_feed),
):
    return templates.TemplateResponse(
        name="posts/feed.html",
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
