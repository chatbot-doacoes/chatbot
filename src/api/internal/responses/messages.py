from src.api.base_response import BaseResponse
from src.models.message import MessageModel


class GetAllMessagesResponse(BaseResponse):
    messages: list[MessageModel]
