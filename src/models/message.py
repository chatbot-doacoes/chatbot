from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel
from typing import ClassVar


class MessageTag(str, Enum):
    DIAPERS = "diapers"
    FOOD = "food"
    CLOTHING = "clothing"


class MessageModel(BaseModel):
    TABLE_NAME: ClassVar[str] = "messages"

    class Cols:
        id = "id"
        institution_id = "institution_id"
        tag = "tag"
        message_template = "message_template"
        donation_url = "donation_url"
        created_at = "created_at"
        update_at = "update_at"

    id: UUID | None = None
    institution_id: UUID
    tag: MessageTag
    message_template: str
    donation_url: str | None = None
    created_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True

    def to_insert_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_at", "update_at"}, mode="json")
