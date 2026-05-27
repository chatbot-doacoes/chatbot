from fastapi import APIRouter, Request, status, Depends
from src.api.dependencies.validations import verify_internal_api_key
from src.models.institution import InstitutionModel
from src.api.exceptions import APIException
from src.api.internal.responses.institutions import GetAllInstitutionsResponse, UpdateInstitutionResponse, RegisterInstitutionResponse
from src.api.internal.payloads.institutions import RegisterInstitution, UpdateInstitution
from src.utils.utils import api_response, hash_api_key, generate_api_key
from src.clients.supabase_client import Supabase
from uuid import UUID

router = APIRouter()

@router.post(
    "/institutions",
    response_model=RegisterInstitutionResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_internal_api_key)]
)
def register_institution(
    payload: RegisterInstitution,
    request: Request
) -> RegisterInstitutionResponse:

    logger = request.state.logger

    logger.add_step("Starting institution registration")

    supabase_client = Supabase(logger)

    api_key = generate_api_key()

    institution = InstitutionModel(
        institution_name=payload.institution_name,
        key_hash=hash_api_key(api_key),
        is_active=True,
    )

    created_institution = supabase_client.register_institution(institution)

    if created_institution is None:

        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Failed to register institution"
        )

    logger.add_step("Institution registered successfully")

    return RegisterInstitutionResponse(
        status_code=status.HTTP_201_CREATED,
        message="Institution registered successfully",
        institution=created_institution,
        api_key=api_key,
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