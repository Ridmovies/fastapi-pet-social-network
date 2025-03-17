from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    model = None

    @classmethod
    async def get_all(cls, session: AsyncSession, order_by=None, options=None, **filter_by):
        query = select(cls.model).filter_by(**filter_by)

        if order_by is not None:
            query = query.order_by(order_by)

        if options is not None:
            for option in options:
                query = query.options(option)

        result = await session.execute(query)
        return result.scalars().unique().all()


    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    # @classmethod
    # async def get_one_by_id(cls, session: AsyncSession, model_id: int):
    #     query = select(cls.model).filter_by(id=int(model_id))
    #     result = await session.execute(query)
    #     return result.scalar_one_or_none()

    @classmethod
    async def get_one_by_id(cls, session: AsyncSession, model_id: int, options=None):
        query = select(cls.model).filter_by(id=int(model_id))
        if options is not None:
            for option in options:
                query = query.options(option)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def create(cls, session: AsyncSession, data, user_id: int):
        data_dict = data.model_dump()
        instance = cls.model(**data_dict, user_id=user_id)
        session.add(instance)
        await session.commit()
        return instance

    @classmethod
    async def delete(cls, session: AsyncSession, model_id: int, user_id: int):
        query = select(cls.model).filter_by(id=model_id, user_id=user_id)
        result = await session.execute(query)
        instance = result.scalar_one_or_none()
        if instance and instance.user_id == user_id:
            await session.delete(instance)
            await session.commit()

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        model_id: int,
        update_data,
        user_id: int,
    ):
        query = select(cls.model).filter_by(id=model_id, user_id=user_id)
        result = await session.execute(query)
        instance = result.scalar_one_or_none()
        if instance:
            for key, value in update_data.model_dump().items():
                setattr(instance, key, value)
            await session.commit()
            return instance
        else:
            raise Exception("No such instance")

    @classmethod
    async def patch(cls, session: AsyncSession, model_id: int, update_data):
        query = select(cls.model).filter_by(id=int(model_id))
        result = await session.execute(query)
        instance = result.scalar_one_or_none()
        if instance:
            for key, value in update_data.model_dump(exclude_unset=True).items():
                setattr(instance, key, value)
            await session.commit()
            return instance
        else:
            raise Exception("No such instance")

    @classmethod
    async def insert(cls, session: AsyncSession, **data):
        instance = cls.model(**data)
        session.add(instance)
        await session.commit()
        return instance


# from sqlalchemy import select
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database import async_session
#
#
# class BaseService:
#     model = None
#
#     @classmethod
#     async def get_all(cls, order_by=None, **filter_by):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(**filter_by)
#             # if order_by:
#             if order_by is not None:
#                 query = query.order_by(order_by)
#             result = await session.execute(query)
#             return result.scalars().all()
#
#
#     @classmethod
#     async def get_one_or_none(cls, **filter_by):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(**filter_by)
#             result = await session.execute(query)
#             return result.scalar_one_or_none()
#
#     @classmethod
#     async def get_one_by_id(cls, model_id: int):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(id=int(model_id))
#             result = await session.execute(query)
#             return result.scalar_one_or_none()
#
#
#     @classmethod
#     async def create(cls, data):
#         async with async_session() as session:
#             data_dict = data.model_dump()
#             instance = cls.model(**data_dict)
#             session.add(instance)
#             await session.commit()
#             return instance
#
#
#     @classmethod
#     async def delete(cls, model_id: int):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(id=int(model_id))
#             result = await session.execute(query)
#             instance = result.scalar_one_or_none()
#             if instance:
#                 await session.delete(instance)
#                 await session.commit()
#
#
#     @classmethod
#     async def update(cls, model_id: int, update_data):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(id=int(model_id))
#             result = await session.execute(query)
#             instance = result.scalar_one_or_none()
#             if instance:
#                 for key, value in update_data.model_dump().items():
#                     setattr(instance, key, value)
#                 await session.commit()
#                 return instance
#             else:
#                 raise Exception('No such instance')
#
#
#     @classmethod
#     async def patch(cls, model_id: int, update_data):
#         async with async_session() as session:
#             query = select(cls.model).filter_by(id=int(model_id))
#             result = await session.execute(query)
#             instance = result.scalar_one_or_none()
#             if instance:
#                 for key, value in update_data.model_dump(exclude_unset=True).items():
#                     setattr(instance, key, value)
#                 await session.commit()
#                 return instance
#             else:
#                 raise Exception('No such instance')
#
#     @classmethod
#     async def insert(cls, **data):
#         async with async_session() as session:
#             instance = cls.model(**data)
#             session.add(instance)
#             await session.commit()
#             return instance
