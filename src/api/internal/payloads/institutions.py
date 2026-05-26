from pydantic import BaseModel


class RegisterInstitution(BaseModel):
    institution_name: str

#pode atualizar o nome da instituição e o status de ativo ou inativo
class UpdateInstitution(BaseModel):
    institution_name: str | None = None
    is_active: bool | None = None