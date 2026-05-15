from fastapi import APIRouter, status
from src.api.internal.payloads.institutions import RegisterInstitution
from src.utils.utils import api_response


router = APIRouter()

@router.post("/institutions")
def send_message(payload:RegisterInstitution):
    return api_response(
        status_code=status.HTTP_201_CREATED,
        message=payload.institution_name
    )