from fastapi import APIRouter, UploadFile, File
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from starlette import status

from src.auth2.jwt_utils import UserDep
from src.database import SessionDep
from src.posts.models import Post, Comment
from src.posts.schemas import CommentCreate, CommentRead, PostCreate
from src.posts.service import PostService, CommentService

router = APIRouter(prefix="/post", tags=["post"])


@router.get("")
async def get_all_posts(session: SessionDep):
    return await PostService.get_all(
        session,
        order_by=desc("id"),
        options=[
            joinedload(Post.user),
            joinedload(Post.likes),
            joinedload(Post.comments),
        ],
    )


@router.get("/{post_id}")
async def get_post(session: SessionDep, post_id: int):
    return await PostService.get_one_by_id(session, post_id)


@router.get("/{post_id}/details")
async def get_post_details(session: SessionDep, post_id: int):
    return await PostService.get_one_by_id(
        session, post_id, options=[joinedload(Post.comments).joinedload(Comment.user), joinedload(Post.likes)]
    )


@router.post("")
async def create_post(
    session: SessionDep,
    post_data: PostCreate,
    user: UserDep,
):
    return await PostService.create_post(session, post_data, user.id)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(session: SessionDep, post_id: int, user: UserDep):
    return await PostService.delete(session, post_id, user.id)


@router.patch("/{post_id}")
async def patch_post(
    session: SessionDep,
    post_data: PostCreate,
    post_id: int,
    user: UserDep,
):
    return await PostService.patch(
        session=session, model_id=post_id, update_data=post_data, user_id=user.id
    )


### Like


@router.post("/{post_id}/like", status_code=status.HTTP_204_NO_CONTENT)
async def like_post(session: SessionDep, post_id: int, user: UserDep):
    return await PostService.like(session, post_id, user.id)


# @router.delete("/{post_id}/unlike", status_code=status.HTTP_204_NO_CONTENT)
# async def unlike_post(session: SessionDep, post_id: int, user: UserDep):
#     return await PostService.unlike(session, post_id, user.id)


### Comments
@router.post("/{post_id}/comment", status_code=status.HTTP_201_CREATED)
async def create_comment(
    session: SessionDep, user: UserDep, post_id: int, comment_data: CommentCreate
):
    return await CommentService.create_comment(session, user.id, post_id, comment_data)


@router.delete("/{post_id}/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(session: SessionDep, user: UserDep, post_id: int, comment_id: int):
    return await CommentService.delete_comment(session, user.id, comment_id)