from src.events.models import Event
from src.services import BaseService


class EventService(BaseService):
    model = Event