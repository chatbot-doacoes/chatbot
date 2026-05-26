from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class RegisterInstitution(BaseModel):
    institution_name: str
