from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

from src.gym.models import MuscleGroup


class GymWorkoutBase(BaseModel):
    name: str
    workout_date: datetime = datetime.now()
    description: Optional[str] = None
    difficulty: Optional[str] = None
    equipment: Optional[str] = None

class GymWorkoutCreate(GymWorkoutBase):
    pass

class GymWorkoutRead(GymWorkoutBase):
    id: int
    exercises: list["ExerciseRead"]

### Exercise

class ExerciseBase(BaseModel):
    name: str
    gym_workout_id: int
    description: Optional[str] = None
    muscle_group: Optional[MuscleGroup] = MuscleGroup.FULL_BODY


class ExerciseCreate(ExerciseBase):
    pass

class ExerciseRead(ExerciseBase):
    id: int
    sets: list["ExerciseSetRead"]


### ExerciseSet

class ExerciseSetBase(BaseModel):
    exercise_id: int
    reps: int | None
    weight: float | None
    duration: int | None
    order: int


class ExerciseSetCreate(ExerciseSetBase):
    pass

class ExerciseSetRead(ExerciseSetBase):
    pass