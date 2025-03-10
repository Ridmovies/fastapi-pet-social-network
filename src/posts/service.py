from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.posts.models import Post
from src.services import BaseService


class PostService(BaseService):
    model = Post

    @classmethod
    async def get_all_posts(cls, session, order_by=None, options=None, **filter_by):
        query = select(Post).filter_by(**filter_by)
        if options:
            query = query.options(*options)  # Применяем переданные опции
        if order_by is not None:
            query = query.order_by(order_by)
        result = await session.execute(query)
        return result.scalars().all()