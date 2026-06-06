from pydantic import BaseModel, HttpUrl
from src.models.message import MessageTag

class RegisterMessage(BaseModel):
    tag: MessageTag
    message_template: str
    donation_url: HttpUrl

class UpdateMessage(BaseModel):
    tag: MessageTag | None = None
    message_template: str | None = None
    donation_url: HttpUrl | None = None
