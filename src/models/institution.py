from datetime import datetime
from pydantic import BaseModel


class InstitutionModel(BaseModel):
    id: int | None = None
    institution_name: str
    key_hash: str
    is_active: bool = True
    created_at: datetime | None = None

    class Config:
        from_attributes = True

    def to_insert_dict(self) -> dict:
        return self.model_dump(exclude={"id", "created_at"})
