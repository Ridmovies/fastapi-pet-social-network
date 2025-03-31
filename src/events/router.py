

from fastapi import APIRouter
from sqlalchemy.orm import joinedload

from src.auth2.jwt_utils import UserDep

from src.database import SessionDep
from src.events.models import Event
from src.events.schemas import EventCreate
from src.events.service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def get_all_events(session: SessionDep):
    return await EventService.get_all(
        session=session, options=[joinedload(Event.comments)]
    )

@router.post("")
async def create_event(session: SessionDep, user: UserDep, data: EventCreate):
    return await EventService.create(session=session, user_id=user.id, data=data)


@router.delete("/{event_id}")
async def delete_event(session: SessionDep, event_id: int, user: UserDep):
    return await EventService.delete(session=session, user_id=user.id, model_id=event_id)


@router.get("/{event_id}")
async def get_event_details(session: SessionDep, event_id: int):
    return await EventService.get_one_by_id(
        session=session, model_id=event_id
    )


#
# @router.post("{community_id}/join")
# async def join_existing_community(
#         community_id: int,
#         session: SessionDep,
#         user: UserDep,
# ):
#     return await CommunityMemberService.join_community(session, user.id, community_id)
