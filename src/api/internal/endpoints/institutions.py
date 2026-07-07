from fastapi import APIRouter, Request, Depends
from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.institutions import GetAllInstitutionsResponse, UpdateInstitutionResponse
from src.api.internal.payloads.institutions import RegisterInstitution, UpdateInstitution
from src.services.institution_service import InstitutionService
from src.api.dependencies.core import get_institution_service
from uuid import UUID

from src.utils.utils import api_response

router = APIRouter()


@router.post(
    "/institutions",
    response_model=BaseResponse,
    status_code=ResponsesEnum.INSTITUTION_CREATED.status_code,
    responses={
        ResponsesEnum.INSTITUTION_CREATED.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.INSTITUTION_CREATED.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.INSTITUTION_CREATED.status_code,
                        "message": ResponsesEnum.INSTITUTION_CREATED.message,
                    }
                }
            }
        },
        ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.status_code,
                        "message": ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.message
                    }
                }
            }
        }
    }
)
def register_institution(
    payload: RegisterInstitution,
    request: Request,
    institution_service: InstitutionService = Depends(get_institution_service)
) -> JSONResponse:

    logger = request.state.logger

    logger.add_step("Starting institution registration")

    institution_created = institution_service.register_institution(payload)

    if not institution_created:
        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.status_code,
            message=ResponsesEnum.FAILED_TO_CREATE_INSTITUTION.message
        )

    logger.add_step("Institution registered successfully")

    return api_response(
        status_code=ResponsesEnum.INSTITUTION_CREATED.status_code,
        response=BaseResponse(
            status_code=ResponsesEnum.INSTITUTION_CREATED.status_code,
            message=ResponsesEnum.INSTITUTION_CREATED.message,
        )
    )


@router.get("/institutions",
            response_model=GetAllInstitutionsResponse,
            responses={
                ResponsesEnum.INSTITUTIONS_FETCHED.status_code: {
                    "model": GetAllInstitutionsResponse,
                    "description": ResponsesEnum.INSTITUTIONS_FETCHED.message,
                },
                ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.status_code: {
                    "model": BaseResponse,
                    "description": ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.message,
                }
            })
def get_institutions(
    request: Request,
    institution_service: InstitutionService = Depends(get_institution_service)
) -> JSONResponse:
    try:
        institutions = institution_service.get_all_institutions()
    except Exception as e:
        request.state.logger.add_step(f"Failed to get institutions: {str(e)}")
        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.status_code,
            message=ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.message
        )

    return api_response(
        status_code=ResponsesEnum.INSTITUTIONS_FETCHED.status_code,
        response=GetAllInstitutionsResponse(
            status_code=ResponsesEnum.INSTITUTIONS_FETCHED.status_code,
            message=ResponsesEnum.INSTITUTIONS_FETCHED.message,
            institutions=institutions
        )
    )

@router.patch(
    "/institutions/{institution_id}",
    response_model=UpdateInstitutionResponse,
    responses={
        ResponsesEnum.INSTITUTION_UPDATED.status_code: {
            "model": UpdateInstitutionResponse,
            "description": ResponsesEnum.INSTITUTION_UPDATED.message,
        },
        ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.NO_FIELDS_TO_UPDATE.message,
        },
        ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.message,
        }
    }
)
def update_institution(
    institution_id: UUID,
    payload: UpdateInstitution,
    request: Request,
    institution_service: InstitutionService = Depends(get_institution_service)
) -> JSONResponse:

    update_data = payload.model_dump(exclude_none=True)

    if not update_data:
        raise APIException(
            status_code=ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code,
            message=ResponsesEnum.NO_FIELDS_TO_UPDATE.message
        )

    try:
        institution = institution_service.update_institution(str(institution_id), update_data)
    except Exception as e:
        request.state.logger.add_step(
            f"Failed to update institution: {str(e)}"
        )

        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.status_code,
            message=ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.message
        )

    return api_response(
        status_code=ResponsesEnum.INSTITUTION_UPDATED.status_code,
        response=UpdateInstitutionResponse(
            status_code=ResponsesEnum.INSTITUTION_UPDATED.status_code,
            message=ResponsesEnum.INSTITUTION_UPDATED.message,
            institution=institution
    ))
