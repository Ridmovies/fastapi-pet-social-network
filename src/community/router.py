from fastapi import APIRouter

from src.auth.dependencies import UserDep
from src.community.models import CommunityMember
from src.community.schemas import CommunityCreate
from src.community.service import CommunityService, CommunityMemberService
from src.database import SessionDep

router = APIRouter(prefix="/community", tags=["community"])


@router.get("")
async def get_all_communities(session: SessionDep):
    return await CommunityService.get_all(session)


@router.post("")
async def create_community(session: SessionDep, user: UserDep, data: CommunityCreate):
    return await CommunityService.create_community(session, user.id, data)


@router.post("{community_id}/join")
async def join_existing_community(community_id: int, session: SessionDep, user: UserDep,):
    return await CommunityMemberService.join_community(session, user.id, community_id)