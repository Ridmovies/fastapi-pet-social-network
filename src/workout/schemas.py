from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WorkoutBase(BaseModel):
    user_id: int
    created_at: datetime
    type: Enum = Enum("walk")

class RunBase(BaseModel):
    distance_km: float
    duration_min: float
    avg_speed_kmh: float

class BicycleBase(BaseModel):
    distance_km: float
    duration_min: float
    avg_speed_kmh: float

class WalkBase(BaseModel):
    distance_km: float
    duration_min: float
    avg_speed_kmh: float

class WorkoutCreate(WorkoutBase):
    run: Optional[RunBase] = None
    bicycle: Optional[BicycleBase] = None
    walk: Optional[WalkBase] = None

class Workout(WorkoutBase):
    id: int
    run: Optional[RunBase] = None
    bicycle: Optional[BicycleBase] = None
    walk: Optional[WalkBase] = None