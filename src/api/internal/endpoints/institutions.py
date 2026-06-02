from fastapi import APIRouter, Request, Depends
from starlette.responses import JSONResponse

from src.models.institution import InstitutionModel
from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.institutions import GetAllInstitutionsResponse, UpdateInstitutionResponse, DeleteInstitutionResponse
from src.api.internal.payloads.institutions import RegisterInstitution, UpdateInstitution
from src.clients.supabase_client import Supabase
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
    request: Request
) -> JSONResponse:

    logger = request.state.logger

    logger.add_step("Starting institution registration")

    supabase_client = Supabase(logger)

    institution = InstitutionModel(
        institution_name=payload.institution_name,
        key_hash=payload.key_hash,
        is_active=True,
    )

    institution_created = supabase_client.register_institution(
        institution
    )

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
                    "content": {
                        "application/json": {
                            "example": {
                                "status_code": ResponsesEnum.INSTITUTIONS_FETCHED.status_code,
                                "message": ResponsesEnum.INSTITUTIONS_FETCHED.message,
                                "institutions": [
                                    {
                                        "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                                        "institution_name": "Institution 1",
                                        "is_active": True,
                                        "created_at": "2023-10-27T10:00:00Z",
                                        "update_at": "2023-10-27T10:00:00Z"
                                    },
                                    {
                                        "id": "b2c3d4e5-f6a7-8901-2345-67890abcdef0",
                                        "institution_name": "Institution 2",
                                        "is_active": False,
                                        "created_at": "2023-10-26T12:30:00Z",
                                        "update_at": "2023-10-26T12:30:00Z"
                                    }
                                ]
                            }
                        }
                    }
                },
                ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.status_code: {
                    "model": BaseResponse,
                    "description": ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.message,
                    "content": {
                        "application/json": {
                            "example": {
                                "status_code": ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.status_code,
                                "message": ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.message
                            }
                        }
                    }
                }
            })
def get_institutions(request: Request) -> JSONResponse:
    supabase_client = Supabase(request.state.logger)

    try:
        institutions = supabase_client.get_institutions()
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
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.INSTITUTION_UPDATED.status_code,
                        "message": ResponsesEnum.INSTITUTION_UPDATED.message,
                        "institution": {
                            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                            "institution_name": "Updated Institution",
                            "is_active": True,
                            "created_at": "2023-10-27T10:00:00Z",
                            "update_at": "2023-10-28T14:30:00Z"
                        }
                    }
                }
            }
        },
        ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.NO_FIELDS_TO_UPDATE.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code,
                        "message": ResponsesEnum.NO_FIELDS_TO_UPDATE.message
                    }
                }
            }
        },
        ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.status_code,
                        "message": ResponsesEnum.FAILED_TO_UPDATE_INSTITUTION.message
                    }
                }
            }
        }
    }
)
def update_institution(
    institution_id: UUID,
    payload: UpdateInstitution,
    request: Request
) -> JSONResponse:

    supabase_client = Supabase(request.state.logger)

    update_data = payload.model_dump(exclude_none=True)

    if not update_data:
        raise APIException(
            status_code=ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code,
            message=ResponsesEnum.NO_FIELDS_TO_UPDATE.message
        )

    try:
        institution = supabase_client.update_institution(
            institution_id=str(institution_id),
            data=update_data
        )
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

@router.delete(
    "/institutions/{institution_id}",
    response_model=DeleteInstitutionResponse,
    responses={
        ResponsesEnum.INSTITUTION_DELETED.status_code: {
            "model": DeleteInstitutionResponse,
            "description": ResponsesEnum.INSTITUTION_DELETED.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.INSTITUTION_DELETED.status_code,
                        "message": ResponsesEnum.INSTITUTION_DELETED.message,
                        "institution": {
                            "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
                            "institution_name": "Institution 1",
                            "is_active": True,
                            "created_at": "2023-10-27T10:00:00Z",
                            "update_at": "2023-10-27T10:00:00Z"
                        }
                    }
                }
            }
        },

        ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.status_code: {
            "model": BaseResponse,
            "description": ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.message,
            "content": {
                "application/json": {
                    "example": {
                        "status_code": ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.status_code,
                        "message": ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.message
                    }
                }
            }
        }
    },
)
def delete_institution(
    institution_id: UUID,
    request: Request
) -> DeleteInstitutionResponse:

    logger = request.state.logger

    supabase_client = Supabase(logger)

    try:

        institution = supabase_client.delete_institution(
            institution_id=str(institution_id)
        )

    except Exception as e:

        logger.add_step(
            f"Failed to delete institution: {str(e)}"
        )

        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.status_code,
            message=ResponsesEnum.FAILED_TO_DELETE_INSTITUTION.message
        )

    return DeleteInstitutionResponse(
        status_code=ResponsesEnum.INSTITUTION_DELETED.status_code,
        message=ResponsesEnum.INSTITUTION_DELETED.message,
        institution=institution
    )
