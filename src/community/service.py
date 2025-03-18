from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.community.models import Community, CommunityMember
from src.services import BaseService


class CommunityService(BaseService):
    model = Community

    @classmethod
    async def create_community(cls, session: AsyncSession, user_id: int, data):
        data_dict = data.model_dump()
        instance = cls.model(**data_dict, creator_id=user_id)
        session.add(instance)
        await session.commit()
        return instance


class CommunityMemberService(BaseService):
    model = CommunityMember

    @classmethod
    async def join_community(
        cls, session: AsyncSession, user_id: int, community_id: int
    ):
        instance = cls.model(user_id=user_id, community_id=community_id)
        session.add(instance)
        await session.commit()
        return instance

    # @classmethod
    # async def leave_community(cls, session: AsyncSession, user_id: int, community_id: int):
    #     query = select(cls.model).filter_by(id=community_id, user_id=user_id)
    #     result = await session.execute(query)
    #     instance = result.scalar_one_or_none()
    #     if instance and instance.user_id == user_id:
    #         await session.delete(instance)
    #         await session.commit()
