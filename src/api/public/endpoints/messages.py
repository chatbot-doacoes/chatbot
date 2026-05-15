from fastapi import APIRouter, status
from src.api.public.payloads.messages import SendMessages
from src.utils.utils import api_response

router = APIRouter()

@router.post("/messages")
def send_message(payload:SendMessages):
    return api_response(
        status_code=status.HTTP_200_OK,
        message=payload.message
    )