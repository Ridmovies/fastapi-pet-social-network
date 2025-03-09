from fastapi import APIRouter
from sqlalchemy import desc
from starlette import status

from src.database import SessionDep
from src.posts.schemas import PostSchema
from src.posts.service import PostService
from src.users.auth import UserDep

router = APIRouter(prefix="/post", tags=["post"])


@router.get("")
async def get_all_posts(session: SessionDep):
    return await PostService.get_all(session, order_by=desc("id"))


@router.get("/{post_id}")
async def get_post(session: SessionDep, post_id: int):
    return await PostService.get_one_by_id(session, post_id)


@router.post("")
async def create_post(session: SessionDep, post_data: PostSchema, user: UserDep):
    return await PostService.create(session, post_data, user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session: SessionDep, post_id: int, user: UserDep):
    return await PostService.delete(session, post_id, user.id)