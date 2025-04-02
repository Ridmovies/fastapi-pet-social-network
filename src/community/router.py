from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import joinedload


from src.auth2.jwt_utils import UserDep
from src.community.models import CommunityMember, Community
from src.community.schemas import CommunityCreate
from src.community.service import CommunityService, CommunityMemberService
from src.database import SessionDep

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


@router.websocket("{community_id}/chat/ws")
async def websocket_chat(
        websocket: WebSocket,
        community_id: int,
        user: UserDep,
        session: SessionDep
):

    # Проверка членства в сообществе
    member = session.query(CommunityMember).filter(
        CommunityMember.community_id == community_id,
        CommunityMember.user_id == user.id
    ).first()
    if not member:
        await websocket.close(code=1008)
        return

    await websocket.accept()