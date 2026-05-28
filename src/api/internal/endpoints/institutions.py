from fastapi import APIRouter, Request

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.institutions import GetAllInstitutionsResponse
from src.api.internal.payloads.institutions import RegisterInstitution
from src.utils.utils import api_response
from src.clients.supabase_client import Supabase

router = APIRouter()


@router.post("/institutions")
def post_institution(payload: RegisterInstitution):
    return api_response(
        status_code=ResponsesEnum.INSTITUTION_CREATED.status_code,
        message=ResponsesEnum.INSTITUTION_CREATED.message
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
def get_institutions(request: Request) -> GetAllInstitutionsResponse:
    supabase_client = Supabase(request.state.logger)

    try:
        institutions = supabase_client.get_institutions()
    except Exception as e:
        request.state.logger.add_step(f"Failed to get institutions: {str(e)}")
        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.status_code,
            message=ResponsesEnum.FAILED_TO_FETCH_INSTITUTIONS.message
        )

    return GetAllInstitutionsResponse(
        status_code=ResponsesEnum.INSTITUTIONS_FETCHED.status_code,
        message=ResponsesEnum.INSTITUTIONS_FETCHED.message,
        institutions=institutions
    )
