### Comments
from fastapi import APIRouter
from starlette import status

from src.auth.dependencies import UserDep
from src.comments.schemas import CommentCreate
from src.comments.service import CommentService
from src.database import SessionDep


router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
        session: SessionDep,
        user: UserDep,
        comment_data: CommentCreate,
):
    return await CommentService.create_comment(session, user.id, comment_data)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(session: SessionDep, user: UserDep, comment_id: int):
    return await CommentService.delete_comment(session, user.id, comment_id)