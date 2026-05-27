from fastapi import APIRouter, Request, status
from src.api.exceptions import APIException
from src.api.internal.responses.institutions import GetAllInstitutionsResponse, UpdateInstitutionResponse
from src.api.internal.payloads.institutions import RegisterInstitution, UpdateInstitution
from src.utils.utils import api_response
from src.clients.supabase_client import Supabase
from uuid import UUID

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

@router.patch("/institutions/{institution_id}", response_model=UpdateInstitutionResponse)
def update_institution(institution_id: UUID, payload: UpdateInstitution, request: Request) -> UpdateInstitutionResponse:
    supabase_client = Supabase(request.state.logger)

    update_data = payload.model_dump(exclude_none=True)
    if not update_data:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="No fields to update"
        )

    try:
        institution = supabase_client.update_institution(
            institution_id=str(institution_id),
            data=update_data
        )
    except Exception as e:
        request.state.logger.add_step(f"Failed to update institution: {str(e)}")
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to update institution"
        )

    return UpdateInstitutionResponse(
        status_code=status.HTTP_200_OK,
        message="Institution updated successfully",
        institution=institution
    )