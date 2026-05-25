from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import ClassVar


class InstitutionModel(BaseModel):
    TABLE_NAME: ClassVar[str] = "institutions"

    class Cols:
        id = "id"
        institution_name = "institution_name"
        key_hash = "key_hash"
        is_active = "is_active"
        created_at = "created_at"
        update_at = "update_at"


    id: UUID | None = None
    institution_name: str
    key_hash: str = Field(min_length=64, max_length=64)
    is_active: bool = False
    created_at: datetime | None = None
    update_at: datetime | None = None

    class Config:
        from_attributes = True

    def to_insert_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_at", "update_at"})
