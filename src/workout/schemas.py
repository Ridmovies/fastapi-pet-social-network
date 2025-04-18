
from pydantic import BaseModel
from typing import Optional



# Базовая модель для активности
class ActivityBase(BaseModel):
    distance_km: float
    duration_sec: int
    avg_speed_kmh: float



# Модели для подтипов активности
class RunBase(ActivityBase):
    pass

class BicycleBase(ActivityBase):
    pass

class WalkBase(ActivityBase):
    pass

# Модель тренировки
class WorkoutBase(BaseModel):
    title: str | None

# Модель для создания тренировки
class WorkoutCreate(WorkoutBase):
    pass

# Модель для возврата тренировки
class Workout(WorkoutBase):
    id: int
    run: Optional[RunBase] = None
    bicycle: Optional[BicycleBase] = None
    walk: Optional[WalkBase] = None

