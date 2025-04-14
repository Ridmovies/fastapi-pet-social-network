from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field, validator, field_validator
from sqlalchemy import JSON


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
    is_private: bool = False
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


class EventRead(EventBase):
    id: int
    user_id: int
    created_at: datetime
    participants: List[EventParticipation] = []



### EVENT POOL

class EventPollBase(BaseModel):
    event_id: int = Field(..., description="ID мероприятия, к которому относится опрос")
    question: str = Field(..., max_length=255, description="Текст вопроса опроса")
    poll_data: dict = Field(
        default_factory=lambda: {"options": [], "votes": {}},
        description="Данные опроса с вариантами ответов и результатами голосования"
    )

    @field_validator('poll_data')
    def validate_poll_data(cls, v):
        if not isinstance(v, dict):
            raise ValueError("poll_data должен быть словарем")

        if "options" not in v or "votes" not in v:
            raise ValueError("poll_data должен содержать keys 'options' и 'votes'")

        if not isinstance(v["options"], list):
            raise ValueError("options должен быть списком")

        if not isinstance(v["votes"], dict):
            raise ValueError("votes должен быть словарем")

        # Проверка соответствия вариантов и счетчиков
        for option in v["options"]:
            if option not in v["votes"]:
                v["votes"][option] = 0

        # Удаляем лишние варианты в votes
        for option in list(v["votes"].keys()):
            if option not in v["options"]:
                del v["votes"][option]

        return v

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": 1,
                "question": "Вы пойдете на этот ивент?",
                "poll_data": {
                    "options": ["Да", "Нет", "Не знаю"],
                    "votes": {"Да": 0, "Нет": 0, "Не знаю": 0}
                }
            }
        }


class EventPollCreate(EventPollBase):
    pass


class EventPollRead(EventPollBase):
    id: int
