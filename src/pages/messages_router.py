from fastapi import APIRouter, Depends, Request

from src.auth2.jwt_utils import UserDep
from src.messages.router import get_messages_between_users
from src.templates import templates


router = APIRouter(prefix="/messages", tags=["page_messages"])


# @router.get("")
# async def get_user_messages_page(
#         request: Request,
#         messages=Depends(get_messages_between_users)
# ):
#     return templates.TemplateResponse(
#         name="messages/users_messages.html",
#         context={"request": request, "messages": messages},
#     )


@router.get("/{receiver_id}")
async def get_messages_between_users_page(
        request: Request,
        user: UserDep,
        receiver_id: int,
        messages=Depends(get_messages_between_users)
):
    return templates.TemplateResponse(
        name="messages/users_messages.html",
        context={"request": request, "messages": messages, "user": user}
    )