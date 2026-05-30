from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.middlewares.ip_allowlist import set_ip_allowlist
from src.api.middlewares.logging_middleware import set_logging_middleware
from src.api.public.router import public_router
from src.api.internal.router import internal_router
from src.api.exceptions import APIException
from src.utils.utils import api_response

app = FastAPI(title="Chatbot API")
set_logging_middleware(app)
set_ip_allowlist(app)

app.include_router(internal_router)
app.include_router(public_router)

@app.exception_handler(APIException)
def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return api_response(
        status_code=exc.status_code,
        message=exc.message,
    )

@app.exception_handler(RequestValidationError)
def api_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return api_response(
        status_code=ResponsesEnum.INVALID_FIELDS.status_code,
        message=ResponsesEnum.INVALID_FIELDS.message
    )

@app.get("/health-check", response_model=BaseResponse)
def health_check() -> BaseResponse:
    return BaseResponse(
        status_code=ResponsesEnum.HEALTH_CHECK_OK.status_code,
        message=ResponsesEnum.HEALTH_CHECK_OK.message
    )

