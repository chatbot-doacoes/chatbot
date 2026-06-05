from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.internal.payloads.user import User
from src.clients.supabase_client import Supabase
from src.utils.utils import check_password, api_response

router = APIRouter()

@router.post("/user/login")
def login(payload: User, request: Request) -> JSONResponse:
    logger = request.state.logger

    supabase_client = Supabase(logger)

    password_hash = supabase_client.get_user(payload.username)
    if not password_hash:
        return api_response(
            status_code=ResponsesEnum.AUTHENTICATION_FAILED.status_code,
            response=BaseResponse(
                status_code=ResponsesEnum.AUTHENTICATION_FAILED.status_code,
                message=ResponsesEnum.AUTHENTICATION_FAILED.message
            )
        )

    password_hash_bytes = password_hash.encode("utf-8")

    if not check_password(
        password=payload.password,
        password_hash=password_hash_bytes
    ):
        return api_response(
            status_code=ResponsesEnum.AUTHENTICATION_FAILED.status_code,
            response=BaseResponse(
                status_code=ResponsesEnum.AUTHENTICATION_FAILED.status_code,
                message=ResponsesEnum.AUTHENTICATION_FAILED.message
            )
        )

    return api_response(
        status_code=ResponsesEnum.AUTHENTICATION_SUCCESS.status_code,
        response=BaseResponse(
            status_code=ResponsesEnum.AUTHENTICATION_SUCCESS.status_code,
            message=ResponsesEnum.AUTHENTICATION_SUCCESS.message
        )
    )

