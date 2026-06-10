from typing import Any

from pydantic import BaseModel, field_validator, ValidationError, Field

from src.api.exceptions import APIException
from src.models.message import MessageTag
from src.api.enum.responses_enum import ResponsesEnum

class User(BaseModel):
    user_name: str = Field(min_length=1, max_length=256)
    user_phone: str = Field(min_length=11, max_length=11)
    tag: MessageTag
    institution: str
    amount: float
    birthdate: str

    @field_validator("user_phone")
    @classmethod
    def validate_phone_number(cls, user_phone: str) -> str:
        if not user_phone.isdigit():
            raise ValueError("phone number must contain only digits.")
        return user_phone

    class Config:
        use_enum_values = True

class SendMessages(BaseModel):
    send_to: list[dict[str, Any]]

    @field_validator("send_to")
    @classmethod
    def validate_send_to(cls, users: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not users:
            raise APIException(
                status_code=ResponsesEnum.INVALID_FIELDS.status_code,
                message=ResponsesEnum.INVALID_FIELDS.message,
            )
        return users

    def split_users(self) -> tuple[list[User], list[dict[str, Any]]]:
        valid_users: list[User] = []
        invalid_users: list[dict[str, Any]] = []

        for user_data in self.send_to:
            try:
                valid_users.append(User.model_validate(user_data))
            except ValidationError as e:
                error_details = e.errors()[0]
                field = error_details["loc"][0]
                message = error_details["msg"]
                user_data["reason"] = f'Field "{field}": {message}.'
                invalid_users.append(user_data)

        return valid_users, invalid_users


