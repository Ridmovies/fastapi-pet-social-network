from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from src.auth2.jwt_utils import UserDep

from src.database import SessionDep
from src.events.service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def get_all_events(session: SessionDep):
    return await EventService.get_all(
        session
    )

#
# @router.get("/{community_id}")
# async def get_community_details(session: SessionDep, community_id: int):
#     return await CommunityService.get_one_by_id(
#         session, community_id, options=[joinedload(Community.posts)]
#     )
#
#
# @router.post("")
# async def create_community(session: SessionDep, user: UserDep, data: CommunityCreate):
#     return await CommunityService.create_community(session, user.id, data)
#
#
# @router.post("{community_id}/join")
# async def join_existing_community(
#         community_id: int,
#         session: SessionDep,
#         user: UserDep,
# ):
#     return await CommunityMemberService.join_community(session, user.id, community_id)
