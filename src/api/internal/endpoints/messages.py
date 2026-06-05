from fastapi import APIRouter, Request
from uuid import UUID

from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.api.internal.responses.messages import GetAllMessagesResponse, UpdateMessageResponse
from src.api.internal.payloads.messages import RegisterMessage, UpdateMessage
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
        message_template=payload.message_template,
        donation_url=str(payload.donation_url),
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
    "/messages/{message_id}",
    response_model=BaseResponse
)
def delete_message(
    message_id: UUID,
    request: Request
) -> JSONResponse:

    supabase_client = Supabase(request.state.logger)

    try:

        deleted = supabase_client.delete_message(
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

@router.patch(
    "/messages/{message_id}",
    response_model=UpdateMessageResponse
)
def update_message(
    message_id: UUID,
    payload: UpdateMessage,
    request: Request
) -> JSONResponse:

    supabase_client = Supabase(request.state.logger)

    update_data = payload.model_dump(
        exclude_none=True
    )

    if not update_data:

        raise APIException(
            status_code=ResponsesEnum.NO_FIELDS_TO_UPDATE.status_code,
            message=ResponsesEnum.NO_FIELDS_TO_UPDATE.message
        )

    try:

        message = supabase_client.update_message(
            message_id=str(message_id),
            data=update_data
        )

    except Exception as e:

        request.state.logger.add_step(
            f"Failed to update message: {str(e)}"
        )

        raise APIException(
            status_code=ResponsesEnum.FAILED_TO_UPDATE_MESSAGE.status_code,
            message=ResponsesEnum.FAILED_TO_UPDATE_MESSAGE.message
        )

    return api_response(
        status_code=ResponsesEnum.MESSAGE_UPDATED.status_code,
        response=UpdateMessageResponse(
            status_code=ResponsesEnum.MESSAGE_UPDATED.status_code,
            message=ResponsesEnum.MESSAGE_UPDATED.message,
            message_data=message
        )
    )
