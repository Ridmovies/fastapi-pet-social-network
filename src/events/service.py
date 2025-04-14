from src.events.models import Event, EventPoll
from src.services import BaseService


class EventService(BaseService):
    model = Event


class EventPollService(BaseService):
    model = EventPoll