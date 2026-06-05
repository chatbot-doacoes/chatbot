from datetime import datetime
from typing import ClassVar
from uuid import UUID

from pydantic import BaseModel


class Users(BaseModel):
    TABLE_NAME: ClassVar[str] = "users"

    class Cols:
        id = "id"
        username = "username"
        hash = "hash"
        created_at = "created_at"

    id: UUID | None = None
    username: str
    hash: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True

    def to_insert_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_at"}, mode="json")