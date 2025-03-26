from sqlalchemy import select, exists

from src.database import async_session
from src.users.models import user_to_user


async def check_following(current_user_id: int, target_user_id: int):
    # Проверяем подписку
    async with async_session() as session:
        is_following = await session.scalar(
            select(exists().where(
                user_to_user.c.follower_id == current_user_id,
                user_to_user.c.following_id == target_user_id
            ))
        )
        return is_following