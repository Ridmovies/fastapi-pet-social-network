from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    content: str = Field(min_length=3, max_length=1000)
    community_id: int = Field(default=1)  # Значение по умолчанию
    event_id: int | None = None  # Поле для идентификатора мероприятия


class PostCreate(PostBase):
    image: Optional[UploadFile] = None  # Добавляем поле для изображения

class PostRead(PostBase):
    id: int
