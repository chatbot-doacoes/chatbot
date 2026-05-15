from pydantic import BaseModel


class RegisterInstitution(BaseModel):
    institution_name: str