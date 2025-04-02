from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.messages.models import Message
from src.services import BaseService


class MessageService(BaseService):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, session: AsyncSession, user_id_1: int, user_id_2: int):
        """
        Асинхронно находит и возвращает все сообщения между двумя пользователями.

        Аргументы:
            user_id_1: ID первого пользователя.
            user_id_2: ID второго пользователя.

        Возвращает:
            Список сообщений между двумя пользователями.
        """

        query = (
            select(cls.model)
            .options(
                joinedload(cls.model.sender),
                joinedload(cls.model.receiver)
            )
            .filter(
                or_(
                    and_(cls.model.user_id == user_id_1, cls.model.receiver_id == user_id_2),
                    and_(cls.model.user_id == user_id_2, cls.model.receiver_id == user_id_1)
                )
            )
            .order_by(cls.model.id)
        )

        result = await session.execute(query)
        # Используем unique() чтобы избежать дубликатов из-за joinedload
        return result.unique().scalars().all()