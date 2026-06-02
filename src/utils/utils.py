import hashlib

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.api.base_response import BaseResponse
from src.models.message import MessageModel

def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

def api_response(status_code: int, response: BaseResponse) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump()
    )

def format_message_templates(message_templates: list[dict[str, str]]) -> dict[str, list[str]]:
    formated_messages = {}
    for message_template in message_templates:
        tag = message_template[MessageModel.Cols.tag]
        if tag not in formated_messages:
            formated_messages[tag] = []
        formated_messages[tag].append(message_template[MessageModel.Cols.message_template])
    return formated_messages