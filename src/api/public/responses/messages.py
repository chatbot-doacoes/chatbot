from typing import Any

from src.api.base_response import BaseResponse

class MessagesResponse(BaseResponse):
    invalid_users: list[Any] | None = None
