from fastapi import APIRouter

from src.auth_app.dependencies import UserDep
from src.post_app.schemas import PostSchema
from src.post_app.service import PostService

router = APIRouter(prefix="/post", tags=["post"])

@router.get("")
async def get_all_posts():
    return await PostService.get_all()



@router.get("/{id}")
async def get_post(id: int):
    return await PostService.get_one_by_id(id)


@router.post("")
async def create_post(post_data: PostSchema, user: UserDep):
    return await PostService.create(post_data)

