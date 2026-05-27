import hashlib
import secrets

from fastapi.responses import JSONResponse


def hash_api_key(api_key: str) -> str:
    return hashlib.sha256(api_key.encode("utf-8")).hexdigest()

def generate_api_key() -> str:
    return secrets.token_hex(32)

def api_response(status_code: int, message: str, **data) -> JSONResponse:
    content = {"status_code": status_code, "message": message}
    content.update(data)
    return JSONResponse(
        status_code=status_code,
        content=content
    )