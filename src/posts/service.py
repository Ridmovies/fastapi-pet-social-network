import uuid
from typing import Optional

from fastapi import UploadFile, File, HTTPException, status
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.comments.models import Comment
from src.config import settings
from src.posts.models import Post, Like
from src.services import BaseService
from src.users.models import user_to_user


class PostService(BaseService):
    model = Post

    @classmethod
    async def get_my_feed(cls, session: AsyncSession, user_id: int):
        stmt = (
            select(Post)
            .where(Post.user_id.in_(
                select(user_to_user.c.following_id)
                .where(user_to_user.c.follower_id == user_id)
            ))
            .order_by(desc(Post.id))
            .options(
                joinedload(Post.user),
                selectinload(Post.likes),
                selectinload(Post.comments).joinedload(Comment.user)
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @classmethod
    async def create_post(
            cls,
            session: AsyncSession,
            user_id: int,
            content: str,
            community_id: int,
            image: Optional[UploadFile]
    ):
        """Создание нового поста с обработкой изображения"""
        try:
            image_path = None

            if image and image.filename:  # Явная проверка на наличие файла
                # Проверяем тип файла
                if image.content_type not in settings.ALLOWED_IMAGE_TYPES:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Недопустимый тип файла. Разрешены: {settings.ALLOWED_IMAGE_TYPES}"
                    )

                # Генерируем уникальное имя
                file_ext = image.filename.split('.')[-1]
                filename = f"{uuid.uuid4()}.{file_ext}"
                save_path = settings.images_upload_path / filename

                # Логирование перед сохранением
                print(f"Пытаемся сохранить файл по пути: {save_path}")

                # Сохраняем файл
                contents = await image.read()
                with open(save_path, "wb") as f:
                    f.write(contents)

                image_path = f"{settings.URL_IMAGES_PREFIX}/{filename}"
                # Проверяем что файл действительно сохранился
                if not save_path.exists():
                    raise HTTPException(
                        status_code=500,
                        detail="Файл не был сохранен на диск"
                    )

                print(f"Файл успешно сохранен: {save_path}")

            # Создаем пост
            post = Post(
                content=content,
                community_id=community_id,
                image_path=image_path,  # Может быть None
                user_id=user_id
            )

            session.add(post)
            await session.commit()
            await session.refresh(post)

            return post

        except Exception as e:
            await session.rollback()
            print(f"Ошибка при создании поста: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка при создании поста: {str(e)}"
            )


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


# class CommentService(BaseService):
#     model = Comment
#
#     @classmethod
#     async def create_comment(
#         cls, session: AsyncSession, user_id: int, data: CommentCreate
#     ):
#         """Создание нового комментария"""
#         data_dict = data.model_dump()
#         comment = Comment(**data_dict, user_id=user_id)
#         session.add(comment)
#         await session.commit()
#         return comment
#
#     @classmethod
#     async def delete_comment(cls, session: AsyncSession, user_id: int, comment_id: int):
#         """Удаление комментария"""
#         query = select(Comment).filter_by(id=comment_id, user_id=user_id)
#         result = await session.execute(query)
#         comment: Comment | None = result.scalar_one_or_none()
#         if comment:
#             await session.delete(comment)
#             await session.commit()
#         else:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Comment not found",
#             )
#
