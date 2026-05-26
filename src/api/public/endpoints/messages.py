from fastapi import APIRouter, status

from src.api.base_response import BaseResponse
from src.api.public.payloads.messages import SendMessages
from src.utils.utils import api_response

router = APIRouter()

@router.post("/messages", response_model=BaseResponse)
def send_message(payload:SendMessages) -> BaseResponse:
    return BaseResponse(
        status_code=status.HTTP_200_OK,
        message=payload.message
    )