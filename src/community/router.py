from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from src.auth.dependencies import UserDep, SessionDep
from src.community.models import CommunityMember, Community
from src.community.schemas import CommunityCreate
from src.community.service import CommunityService, CommunityMemberService

router = APIRouter(prefix="/community", tags=["community"])


@router.get("")
async def get_all_communities(session: SessionDep):
    return await CommunityService.get_all(
        session, options=[joinedload(Community.members)]
    )


@router.get("/{community_id}")
async def get_community_details(session: SessionDep, community_id: int):
    return await CommunityService.get_one_by_id(
        session, community_id, options=[joinedload(Community.posts)]
    )


@router.post("")
async def create_community(session: SessionDep, user: UserDep, data: CommunityCreate):
    return await CommunityService.create_community(session, user.id, data)


@router.post("{community_id}/join")
async def join_existing_community(
        community_id: int,
        session: SessionDep,
        user: UserDep,
):
    return await CommunityMemberService.join_community(session, user.id, community_id)
