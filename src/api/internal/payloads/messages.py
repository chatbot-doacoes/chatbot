from pydantic import BaseModel
from src.models.message import MessageTag

class RegisterMessage(BaseModel):
    tag: MessageTag
    message_template: str
