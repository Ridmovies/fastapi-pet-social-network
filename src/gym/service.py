from src.gym.models import GymWorkout, Exercise, ExerciseSet
from src.services import BaseService



class GymWorkoutService(BaseService):
    model = GymWorkout


class ExerciseService(BaseService):
    model = Exercise


class ExerciseSetService(BaseService):
    model = ExerciseSet