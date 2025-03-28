from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class EventParticipationBase(BaseModel):
    user_id: int
    event_id: int
    joined_at: datetime


class EventParticipationCreate(EventParticipationBase):
    pass


class EventParticipation(EventParticipationBase):
    pass


class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    is_private: bool = False
    required_equipment: Optional[str] = None
    skill_level: Optional[str] = None
    status: str = "planned"


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    max_participants: Optional[int] = None
    is_private: Optional[bool] = None
    required_equipment: Optional[str] = None
    skill_level: Optional[str] = None
    status: Optional[str] = None


class Event(EventBase):
    id: int
    user_id: int
    created_at: datetime
    participants: List[EventParticipation] = []