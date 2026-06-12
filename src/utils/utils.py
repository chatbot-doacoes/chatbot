import hashlib

import bcrypt
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.models.message import MessageModel

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

def api_response(status_code: int, response: BaseResponse) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response)
    )

def format_message_templates(message_templates: list[dict[str, str]]) -> dict[str, list[str]]:
    formatted_messages = {}
    for message_template in message_templates:
        tag = message_template[MessageModel.Cols.tag]
        if tag not in formatted_messages:
            formatted_messages[tag] = []
        formatted_messages[tag].append({
            "message_template": message_template[MessageModel.Cols.message_template],
            "donation_url": message_template[MessageModel.Cols.donation_url],
        })
    return formatted_messages

def check_password(password: str, password_hash: str) -> bool:
    password_hash_bytes = password_hash.encode("utf-8")
    password_bytes = password.encode("utf-8")
    return True if bcrypt.checkpw(password_bytes, password_hash_bytes) else False
