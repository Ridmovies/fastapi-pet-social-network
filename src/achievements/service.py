from src.achievements.models import Achievement
from src.services import BaseService


class AchievementService(BaseService):
    model = Achievement