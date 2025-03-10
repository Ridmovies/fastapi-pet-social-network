from fastapi import APIRouter
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from starlette import status

from src.database import SessionDep
from src.posts.models import Post
from src.posts.schemas import PostSchema
from src.posts.service import PostService
from src.users.auth import UserDep

router = APIRouter(prefix="/post", tags=["post"])


@router.get("")
async def get_all_posts(session: SessionDep):
    return await PostService.get_all_posts(
        session,
        order_by=desc("id"),
        options=[joinedload(Post.user)]
    )


@router.get("/{post_id}")
async def get_post(session: SessionDep, post_id: int):
    return await PostService.get_one_by_id(session, post_id)


@router.post("")
async def create_post(session: SessionDep, post_data: PostSchema, user: UserDep):
    return await PostService.create(session, post_data, user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session: SessionDep, post_id: int, user: UserDep):
    return await PostService.delete(session, post_id, user.id)


### Like

@router.post("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_post(session: SessionDep, post_id: int, user: UserDep):
    return await PostService.like(session, post_id, user.id)


# @router.delete("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
# async def unlike_post(session: SessionDep, post_id: int, user: UserDep):
#     return await PostService.unlike(session, post_id, user.id)