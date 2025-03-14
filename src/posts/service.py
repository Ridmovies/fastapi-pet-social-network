from fastapi import UploadFile, File
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.posts.models import Post, Like
from src.services import BaseService


class PostService(BaseService):
    model = Post

    @classmethod
    async def create_post(cls, session, data, user_id):
        """Создание нового поста"""
        data_dict = data.model_dump()
        post = Post(**data_dict, user_id=user_id)
        session.add(post)
        await session.commit()
        return post

    @classmethod
    async def get_all_posts(cls, session, order_by=None, options=None, **filter_by):
        query = select(Post).filter_by(**filter_by)
        if options:
            query = query.options(*options)  # Применяем переданные опции
        if order_by is not None:
            query = query.order_by(order_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def like(cls, session, post_id, user_id):
        query = select(Like).filter_by(post_id=post_id, user_id=user_id)
        result = await session.execute(query)
        likes_exist: Like | None = result.scalar_one_or_none()
        # Если лайка нет, то ставим лайк
        if not likes_exist:
            # # Создаем новый лайк
            new_like: Like = Like(user_id=user_id, post_id=post_id)
            session.add(new_like)
        else:
            # Удаляем лайк
            await session.delete(likes_exist)
        await session.commit()
