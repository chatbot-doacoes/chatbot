from fastapi import APIRouter, status

from src.api.base_response import BaseResponse
from src.api.public.payloads.messages import SendMessages, User

router = APIRouter()

@router.post("/messages", response_model=BaseResponse)
def send_messages(payload: SendMessages) -> BaseResponse:
    return BaseResponse(
        status_code=status.HTTP_200_OK,
        message="message"
    )