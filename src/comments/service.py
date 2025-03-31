from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.comments.models import Comment
from src.comments.schemas import CommentCreate
from src.services import BaseService


class CommentService(BaseService):
    model = Comment

    @classmethod
    async def create_comment(
        cls, session: AsyncSession, user_id: int, data: CommentCreate
    ):
        """Создание нового комментария"""
        data_dict = data.model_dump()
        comment = Comment(**data_dict, user_id=user_id)
        session.add(comment)
        await session.commit()
        return comment

    @classmethod
    async def delete_comment(cls, session: AsyncSession, user_id: int, comment_id: int):
        """Удаление комментария"""
        query = select(Comment).filter_by(id=comment_id, user_id=user_id)
        result = await session.execute(query)
        comment: Comment | None = result.scalar_one_or_none()
        if comment:
            await session.delete(comment)
            await session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

