import json
import logging
from typing import Dict, Tuple

from fastapi import APIRouter, status, WebSocket, WebSocketDisconnect, HTTPException

from src.auth.dependencies import UserDep
from src.database import SessionDep
from src.messages.schemas import MessageRead, MessageCreate
from src.messages.service import MessageService

logger = logging.Logger(__name__)

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



# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: dict[tuple[int, int], WebSocket] = {}
#
#     async def connect(self, websocket: WebSocket, user_id: int, receiver_id: int):
#         key = (min(user_id, receiver_id), max(user_id, receiver_id))
#         self.active_connections[key] = websocket
#
#     def disconnect(self, websocket: WebSocket, user_id: int, receiver_id: int):
#         key = (min(user_id, receiver_id), max(user_id, receiver_id))
#         if key in self.active_connections and self.active_connections[key] == websocket:
#             del self.active_connections[key]
#
#     async def broadcast(self, message: dict, user_id_1: int, user_id_2: int):
#         key = (min(user_id_1, user_id_2), max(user_id_1, user_id_2))
#         if connection := self.active_connections.get(key):
#             try:
#                 await connection.send_json(message)
#             except Exception as e:
#                 print(f"Error sending message: {e}")
#                 self.disconnect(connection, user_id_1, user_id_2)
#
#
# manager = ConnectionManager()


# @router.websocket("/ws/{receiver_id}")
# async def websocket_chat(
#         websocket: WebSocket,
#         receiver_id: int,
#         session: SessionDep,
#         user: WsUserDep,
# ):
#     try:
#         await websocket.accept()
#
#         # Verify user is authorized to chat with receiver_id
#         # Add any additional authorization checks here
#
#         await manager.connect(websocket, user.id, receiver_id)
#
#         try:
#             while True:
#                 try:
#                     data = await websocket.receive_json()
#
#                     if data.get("type") == "message":
#                         message = await MessageService.create(
#                             session=session,
#                             user_id=user.id,
#                             data=MessageCreate(
#                                 content=data["content"],
#                                 receiver_id=receiver_id
#                             )
#                         )
#
#                         await manager.broadcast(
#                             {
#                                 "type": "message",
#                                 "content": message.content,
#                                 "sender": {
#                                     "id": user.id,
#                                     "username": user.username
#                                 },
#                                 "receiver_id": receiver_id,
#                                 "created_at": message.created_at.isoformat(),
#                                 "message_id": message.id,
#                             },
#                             user.id,
#                             receiver_id,
#                         )
#
#                 except json.JSONDecodeError:
#                     await websocket.send_json({"error": "Invalid JSON"})
#                 except KeyError as e:
#                     await websocket.send_json({"error": f"Missing field: {str(e)}"})
#
#         except WebSocketDisconnect as e:
#             print(f"WebSocket disconnected: {e.code} - {e.reason}")
#             await manager.disconnect(websocket, user.id, receiver_id)
#         except Exception as e:
#             print(f"WebSocket error: {e}")
#             await websocket.close(code=1011, reason=str(e))
#
#     except HTTPException as e:
#         print(f"Connection rejected: {e.detail}")
#         await websocket.close(code=e.status_code, reason=e.detail)
#     except Exception as e:
#         print(f"Connection error: {e}")
#         await websocket.close(code=4000, reason="Connection error")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")