from fastapi import APIRouter

from src.posts.schemas import PostSchema
from src.posts.service import PostService

router = APIRouter(prefix="/post", tags=["post"])

@router.get("")
async def get_all_posts():
    return await PostService.get_all()



@router.get("/{id}")
async def get_post(id: int):
    return await PostService.get_one_by_id(id)


@router.post("")
async def create_post(post_data: PostSchema):
    return await PostService.create(post_data)

