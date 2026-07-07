from fastapi import APIRouter, Request, Depends
from uuid import UUID

from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.messages import GetAllMessagesResponse
from src.api.internal.payloads.messages import RegisterMessage
from src.utils.utils import api_response
from src.services.message_service import MessageService
from src.api.dependencies.core import get_message_service

router = APIRouter()

@router.post("/institutions/{institution_id}/messages")
def post_message(
    institution_id: UUID, 
    payload: RegisterMessage, 
    request: Request,
    message_service: MessageService = Depends(get_message_service)
) -> JSONResponse:
    
    try:
        success = message_service.register_message(institution_id, payload)
        if not success:
            raise Exception("Failed to register message in database.")
    except Exception as e:
        request.state.logger.add_step(f"Failed to register message: {str(e)}")
        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_CREATE_MESSAGE.status_code,
            message=ResponsesEnum.FAILED_TO_CREATE_MESSAGE.message
        )

    return api_response(
        status_code=ResponsesEnum.MESSAGE_CREATED.status_code,
        response=BaseResponse(
            status_code=ResponsesEnum.MESSAGE_CREATED.status_code,
            message=ResponsesEnum.MESSAGE_CREATED.message
        )
    )

@router.get("/institutions/{institution_id}/messages",
            response_model=GetAllMessagesResponse,
            responses={
                ResponsesEnum.MESSAGES_FETCHED.status_code: {
                    "model": GetAllMessagesResponse,
                    "description": ResponsesEnum.MESSAGES_FETCHED.message,
                },
                ResponsesEnum.FAILED_TO_FETCH_MESSAGES.status_code: {
                    "model": BaseResponse,
                    "description": ResponsesEnum.FAILED_TO_FETCH_MESSAGES.message,
                }
            })
def get_messages(
    institution_id: UUID, 
    request: Request,
    message_service: MessageService = Depends(get_message_service)
) -> JSONResponse:
    try:
        messages = message_service.get_messages_by_institution(institution_id)
    except Exception as e:
        request.state.logger.add_step(f"Failed to get messages: {str(e)}")
        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_FETCH_MESSAGES.status_code,
            message=ResponsesEnum.FAILED_TO_FETCH_MESSAGES.message
        )

    return api_response(
        status_code=ResponsesEnum.MESSAGES_FETCHED.status_code,
        response=GetAllMessagesResponse(
            status_code=ResponsesEnum.MESSAGES_FETCHED.status_code,
            message=ResponsesEnum.MESSAGES_FETCHED.message,
            messages=messages
        )
    )
