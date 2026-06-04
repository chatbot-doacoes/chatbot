from fastapi import APIRouter, Request
from uuid import UUID

from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.messages import GetAllMessagesResponse
from src.api.internal.payloads.messages import RegisterMessage
from src.utils.utils import api_response
from src.clients.supabase_client import Supabase
from src.models.message import MessageModel

router = APIRouter()

@router.post("/institutions/{institution_id}/messages")
def post_message(institution_id: UUID, payload: RegisterMessage, request: Request) -> JSONResponse:
    supabase_client = Supabase(request.state.logger)

    message_model = MessageModel(
        institution_id=institution_id,
        tag=payload.tag,
        message_template=payload.message_template
    )

    try:
        success = supabase_client.register_message(message_model)
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
def get_messages(institution_id: UUID, request: Request) -> JSONResponse:
    supabase_client = Supabase(request.state.logger)

    try:
        messages = supabase_client.get_messages_by_institution(institution_id)
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

@router.delete(
    "/institutions/{institution_id}/messages/{message_id}",
    response_model=BaseResponse
)
def delete_message(
    institution_id: UUID,
    message_id: UUID,
    request: Request
) -> JSONResponse:

    supabase_client = Supabase(request.state.logger)

    try:

        deleted = supabase_client.delete_message(
            institution_id=str(institution_id),
            message_id=str(message_id)
        )

        if not deleted:
            raise Exception(
                "Message not found."
            )

    except Exception as e:

        request.state.logger.add_step(
            f"Failed to delete message: {str(e)}"
        )

        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_DELETE_MESSAGE.status_code,
            message=ResponsesEnum.FAILED_TO_DELETE_MESSAGE.message
        )

    return api_response(
        status_code=ResponsesEnum.MESSAGE_DELETED.status_code,
        response=BaseResponse(
            status_code=ResponsesEnum.MESSAGE_DELETED.status_code,
            message=ResponsesEnum.MESSAGE_DELETED.message
        )
    )
