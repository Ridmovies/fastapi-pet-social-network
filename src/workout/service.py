
from src.services import BaseService
from src.workout.models import Workout


class WorkoutService(BaseService):
    model = Workout