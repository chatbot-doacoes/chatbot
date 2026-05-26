from fastapi import APIRouter, Request, status
from src.api.internal.responses.institutions import GetAllInstitutionsResponse
from src.api.internal.payloads.institutions import RegisterInstitution
from src.utils.utils import api_response
from src.clients.supabase_client import Supabase

router = APIRouter()

@router.post("/institutions")
def send_message(payload:RegisterInstitution):
    return api_response(
        status_code=status.HTTP_201_CREATED,
        message=payload.institution_name
    )


@router.get("/institutions", response_model=GetAllInstitutionsResponse)
def get_institutions(request: Request) -> GetAllInstitutionsResponse:
    supabase_client = Supabase(request.state.logger)

    institutions = supabase_client.get_institutions()

    return GetAllInstitutionsResponse(
        status_code=status.HTTP_200_OK,
        message="Successfully fetched institutions",
        institutions=institutions
    )