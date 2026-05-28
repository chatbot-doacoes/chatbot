from pydantic import BaseModel, Field, field_validator


class RegisterInstitution(BaseModel):
    institution_name: str = Field(
        min_length=1,
        max_length=255
    )

    @field_validator("institution_name")
    @classmethod
    def validate_institution_name(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Institution name cannot be empty"
            )

        return value

#pode atualizar o nome da instituição e o status de ativo ou inativo
class UpdateInstitution(BaseModel):
    institution_name: str | None = None
    is_active: bool | None = None