from enum import Enum

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Базовая модель для активности
class ActivityBase(BaseModel):
    distance_km: float
    duration_min: float
    avg_speed_kmh: float

# Модель тренировки
class WorkoutBase(BaseModel):
    pass

# Модели для подтипов активности
class RunBase(ActivityBase):
    pass

class BicycleBase(ActivityBase):
    pass

class WalkBase(ActivityBase):
    pass

# Модель для создания тренировки
class WorkoutCreate(WorkoutBase):
    run: Optional[RunBase] = None
    bicycle: Optional[BicycleBase] = None
    walk: Optional[WalkBase] = None

# Модель для возврата тренировки
class Workout(WorkoutBase):
    id: int
    run: Optional[RunBase] = None
    bicycle: Optional[BicycleBase] = None
    walk: Optional[WalkBase] = None

