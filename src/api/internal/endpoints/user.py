from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse

from src.api.internal.payloads.user import User
from src.clients.supabase_client import Supabase
from src.utils.utils import check_password

router = APIRouter()

@router.post("/user/login")
def login(payload: User, request: Request) -> JSONResponse:
    logger = request.state.logger

    supabase_client = Supabase(logger)

    password_hash = supabase_client.get_user(payload.username)
    if not password_hash:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Incorrect username or password."
            }
        )

    password_hash_bytes = password_hash.encode("utf-8")

    if not check_password(
        password=payload.password,
        password_hash=password_hash_bytes
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "status_code": status.HTTP_401_UNAUTHORIZED,
                "message": "Incorrect username or password."
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status_code": status.HTTP_200_OK,
            "message": "Authenticated successfully."
        }
    )

