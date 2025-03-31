### Comments
from fastapi import APIRouter
from starlette import status

from src.auth2.jwt_utils import UserDep
from src.comments.schemas import CommentCreate
from src.database import SessionDep
from src.posts.service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/comment", status_code=status.HTTP_201_CREATED)
async def create_comment(
        session: SessionDep,
        user: UserDep,
        comment_data: CommentCreate,
):
    return await CommentService.create_comment(session, user.id, comment_data)

#
# @router.delete("/{post_id}/comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_comment(session: SessionDep, user: UserDep, post_id: int, comment_id: int):
#     return await CommentService.delete_comment(session, user.id, comment_id)