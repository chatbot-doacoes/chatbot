from pydantic import BaseModel, Field, field_validator


class RegisterInstitution(BaseModel):
    institution_name: str = Field(
        min_length=1,
        max_length=255
    )

    key_hash: str = Field(
        min_length=64,
        max_length=64
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
    
    @field_validator("key_hash")
    @classmethod
    def validate_key_hash(cls, value: str) -> str:

        value = value.strip().lower()

        if len(value) != 64:
            raise ValueError(
                "key_hash must contain 64 characters"
            )

        try:
            int(value, 16)
        except ValueError:
            raise ValueError(
                "key_hash must be a valid hexadecimal SHA-256 hash"
            )

        return value

#pode atualizar o nome da instituição e o status de ativo ou inativo
class UpdateInstitution(BaseModel):
    institution_name: str | None = None
    is_active: bool | None = None