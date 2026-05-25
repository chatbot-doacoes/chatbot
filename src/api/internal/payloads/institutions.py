from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class RegisterInstitution(BaseModel):
    institution_name: str

class InstitutionResponse(BaseModel):
    id: UUID
    institution_name: str
    is_active: bool
    created_at: datetime
    update_at: datetime | None = None

    class Config:
        from_attributes = True