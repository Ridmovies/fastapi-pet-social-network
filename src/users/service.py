# from fastapi import HTTPException
# from sqlalchemy import select, delete
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
# from sqlalchemy.sql.operators import and_
#
# from src.services import BaseService
#
# from src.database import User, user_to_user
# from src.users.pwd_utils import get_password_hash
# from src.users.schemas import UserInSchema
#
#
# class UserService(BaseService):
#     model = User
#
#     @classmethod
#     async def get_all_users(cls, session: AsyncSession):
#         query = select(User).options(selectinload(User.posts), selectinload(User.following))
#         result = await session.execute(query)
#         return result.scalars().all()
#
#
#
#     @classmethod
#     async def create_user(cls, data: UserInSchema, session: AsyncSession) -> User:
#         """Создание нового пользователя"""
#         username = data.username
#         # Проверяем, существует ли пользователь с таким username
#         existing_user = await session.execute(
#             select(User).where(User.username == username)
#         )
#         if existing_user.scalar():
#             raise HTTPException(
#                 status_code=400,
#                 detail="Username already exists"
#             )
#         # Если пользователя нет, создаем нового
#         hashed_password = get_password_hash(data.password)
#         new_user = User(username=username, hashed_password=hashed_password)
#         session.add(new_user)
#         await session.commit()
#         return new_user
#
#
#     @classmethod
#     async def get_user_by_username(cls, session: AsyncSession, username: str) -> User | None:
#         stmt = select(User).where(User.username == username)
#         result = await session.execute(stmt)
#         return result.scalars().one_or_none()
#
#
#     @classmethod
#     async def get_user_by_username_with_following(cls, session: AsyncSession, username: str) -> User | None:
#         stmt = (select(User)
#                 .options(selectinload(User.following)).where(User.username == username))
#         result = await session.execute(stmt)
#         return result.scalars().one_or_none()
#
#
#     @classmethod
#     async def get_user_by_id_with_followers(cls, session: AsyncSession, user_id: int) -> User:
#         stmt = (
#             select(User)
#             .options(selectinload(User.following))  # Загружаем отношение `following`
#             .where(User.id == user_id)
#         )
#         result = await session.execute(stmt)
#         user = result.scalars().one_or_none()
#         return user
#
#
#     @classmethod
#     async def follow_user(
#             cls,
#             session: AsyncSession,
#             follow_user_id: int,
#             current_user: User,
#
#     ):
#         """Подписываемся на пользователя"""
#         # Получить пользователя на которого хотим подписаться по id
#         user_to_follow: User = await UserService.get_one_by_id(session=session, model_id=follow_user_id)
#         if current_user and user_to_follow:
#             from sqlalchemy.exc import IntegrityError
#             try:
#                 # Увеличиваем популярность на 1
#                 # user_to_follow.popularity += 1
#
#                 # Вставка в таблицу новой записи, только если составное значение уникально
#                 ins = user_to_user.insert().values(
#                     follower_id=current_user.id, following_id=user_to_follow.id
#                 )
#                 await session.execute(ins)
#                 await session.commit()
#                 return {"result": True}
#
#             except IntegrityError as e:
#                 return {
#                     "result": False,
#                     "error_type": "IntegrityError",
#                     "error_message": str(e.args),
#                 }
#
#             except Exception as e:
#                 return {
#                     "result": False,
#                     "error_type": "OtherError",
#                     "error_message": str(e),
#                 }
#         return {"result": False}
#
#
#     @classmethod
#     async def unfollow_user(
#             cls,
#             session: AsyncSession,
#             unfollow_user_id: int,
#             current_user: User,
#     ):
#         """Отписка от пользователя по id"""
#         # Получаем пользователя от которого хотим отписаться по id
#         user_to_unfollow: User = await UserService.get_one_by_id(session=session, model_id=unfollow_user_id)
#
#         # Удаление записи из БД
#         query = delete(user_to_user).where(
#             and_(
#                 user_to_user.c.follower_id == current_user.id,
#                 user_to_user.c.following_id == user_to_unfollow.id,
#             )
#         )
#         result = await session.execute(query)
#         # Получаем количество удалемых записей
#         deleted_rows: int = result.rowcount
#
#         if deleted_rows > 0:
#             await session.commit()
#             return {"result": True}
#         else:
#             return {"result": False}