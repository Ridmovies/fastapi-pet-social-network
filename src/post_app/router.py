from fastapi import APIRouter, Request, Depends

from src.auth_app.dependencies import get_current_user
from src.auth_app.models import User
from src.post_app.schemas import PostSchema
from src.post_app.service import PostService

router = APIRouter(prefix="/post", tags=["post"])

@router.get("")
async def get_all_posts(user: User = Depends(get_current_user)):
    print(f"{user=}")
    return await PostService.get_all()



@router.get("/{id}")
async def get_post(id: int):
    return await PostService.get_one_by_id(id)


@router.post("")
async def create_post(post_data: PostSchema):
    return await PostService.create(post_data)

