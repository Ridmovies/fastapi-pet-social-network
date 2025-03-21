from src.messages.models import Message
from src.services import BaseService


class MessageService(BaseService):
    model = Message