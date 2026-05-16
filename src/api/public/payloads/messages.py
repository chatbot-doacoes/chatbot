from pydantic import BaseModel


class SendMessages(BaseModel):
    message: str

