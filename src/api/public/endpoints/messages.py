import random
from typing import Any

from fastapi import APIRouter, status, Request, Header
from starlette.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.public.payloads.messages import SendMessages, User
from src.api.public.responses.messages import MessagesResponse
from src.clients.supabase_client import Supabase
from src.clients.twilio_client import Twilio
from src.utils.utils import hash_api_key, format_message_templates, api_response

router = APIRouter()

@router.post("/messages", response_model=BaseResponse)
def send_messages(
        payload: SendMessages,
        request: Request,
        api_key: str = Header(alias="X-API-Key")
) -> JSONResponse:
    valid_users, invalid_users = payload.send_to

    logger = request.state.logger

    supabase_client = Supabase(logger)
    twilio_client = Twilio(logger)

    messages_templates = supabase_client.get_messages_templates(key_hash=hash_api_key(api_key))
    formated_messages = format_message_templates(messages_templates)

    for user in valid_users:
        hello_string = f"Olá {user.user_name}!\n\n"

        template_list = formated_messages.get(user.tag)
        if template_list is None:
            _add_invalid_user(
                user=user,
                reason="The tag is not registered for this institution.",
                invalid_users=invalid_users
            )
            valid_users.remove(user)
            continue

        template = hello_string + random.choice(formated_messages[user.tag])
        if not twilio_client.send_whatsapp_message(
            to_number=user.user_phone,
            message=template
        ):
            _add_invalid_user(
                user=user,
                reason="Internal server error while sending the message.",
                invalid_users=invalid_users
            )
            valid_users.remove(user)

    if not valid_users and invalid_users:
        return api_response(
            status_code=ResponsesEnum.ALL_USERS_INVALID.status_code,
            response=MessagesResponse(
                status_code=ResponsesEnum.ALL_USERS_INVALID.status_code,
                message=ResponsesEnum.ALL_USERS_INVALID.message,
                invalid_users=invalid_users
            )
        )
    elif valid_users and invalid_users:
        return api_response(
            status_code=ResponsesEnum.PARTIALLY_USERS_VALID.status_code,
            response=MessagesResponse(
                status_code=ResponsesEnum.PARTIALLY_USERS_VALID.status_code,
                message=ResponsesEnum.PARTIALLY_USERS_VALID.message,
                invalid_users=invalid_users
            )
        )
    return api_response(
        status_code=ResponsesEnum.ALL_USERS_VALID.status_code,
        response=MessagesResponse(
            status_code=ResponsesEnum.ALL_USERS_VALID.status_code,
            message=ResponsesEnum.ALL_USERS_VALID.message,
        )
    )

def _add_invalid_user(user: User, reason: str, invalid_users: list[Any]) -> None:
    invalid_user = user.model_dump()
    invalid_user["reason"] = reason
    invalid_users.append(invalid_user)