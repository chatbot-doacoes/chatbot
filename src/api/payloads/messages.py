from pydantic import BaseModel


class MessagesPayload(BaseModel):
    message: str

