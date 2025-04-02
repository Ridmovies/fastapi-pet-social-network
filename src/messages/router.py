from fastapi import APIRouter, status

from src.auth2.jwt_utils import UserDep
from src.database import SessionDep
from src.messages.schemas import MessageRead, MessageCreate
from src.messages.service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.get("/", response_model=list[MessageRead])
async def get_user_messages(session: SessionDep, user: UserDep):
    return await MessageService.get_all(session=session, user_id=user.id)


@router.get("/{receiver_id}", response_model=list[MessageRead])
async def get_messages_between_users(session: SessionDep, user: UserDep, receiver_id: int):
    return await MessageService.get_messages_between_users(session=session, user_id_1=user.id, user_id_2=receiver_id)


@router.post("/{receiver_id}", response_model=MessageCreate)
async def create_message(session: SessionDep, user: UserDep, data: MessageCreate):
    return await MessageService.create(
        session=session, user_id=user.id, data=data
    )

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(session: SessionDep, user: UserDep, message_id: int):
    return await MessageService.delete(
        session=session, user_id=user.id, model_id=message_id
    )