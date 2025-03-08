from fastapi import APIRouter

from src.database import SessionDep
from src.posts.schemas import PostSchema
from src.posts.service import PostService

router = APIRouter(prefix="/post", tags=["post"])


@router.get("")
async def get_all_posts(session: SessionDep):
    return await PostService.get_all(session)


@router.get("/{post_id}")
async def get_post(session: SessionDep, post_id: int):
    return await PostService.get_one_by_id(session, post_id)


@router.post("")
async def create_post(session: SessionDep, post_data: PostSchema):
    user_id: int = 1 # TODO: Добавить получение user_id из JWT token
    return await PostService.create(session, post_data, user_id)

