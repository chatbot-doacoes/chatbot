from fastapi import APIRouter, Request, status
from src.api.exceptions import APIException
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

    try:
        institutions = supabase_client.get_institutions()
    except Exception as e:
        request.state.logger.add_step(f"Failed to get institutions: {str(e)}")
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to fetch institutions"
        )

    return GetAllInstitutionsResponse(
        status_code=status.HTTP_200_OK,
        message="Successfully fetched institutions",
        institutions=institutions
    )