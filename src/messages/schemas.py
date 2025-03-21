from datetime import datetime

from pydantic import BaseModel

class MessageBase(BaseModel):
    content: str
    read: bool = False
    receiver_id: int



class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: int
    created_at: datetime
