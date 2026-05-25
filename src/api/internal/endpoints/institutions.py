from fastapi import APIRouter, status
from src.models.institution import InstitutionModel
from src.api.internal.payloads.institutions import RegisterInstitution, InstitutionResponse
from src.utils.utils import api_response
from src.clients.supabase_client import Supabase
from src.utils.logger import Logger

router = APIRouter()

@router.post("/institutions")
def send_message(payload:RegisterInstitution):
    return api_response(
        status_code=status.HTTP_201_CREATED,
        message=payload.institution_name
    )


@router.get("/institutions", response_model=list[InstitutionResponse])
def get_institutions():
    logger = Logger()
    supabase_client = Supabase(logger)

    institutions = supabase_client.get_institutions()

    return api_response(
        status_code=status.HTTP_200_OK,
        message="Institutions fetched",
        data=institutions
    )