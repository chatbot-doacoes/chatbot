from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api.base_response import BaseResponse
from src.api.enum.responses_enum import ResponsesEnum
from src.api.middlewares.ip_allowlist import set_ip_allowlist
from src.api.middlewares.logging_middleware import set_logging_middleware
from src.api.public.router import public_router
from src.api.internal.router import internal_router
from src.api.exceptions import APIException
from src.utils.utils import api_response

app = FastAPI(title="Chatbot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
set_logging_middleware(app)
set_ip_allowlist(app)

app.include_router(internal_router)
app.include_router(public_router)

@app.exception_handler(APIException)
def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return api_response(
        status_code=exc.status_code,
        response=BaseResponse(
            status_code=exc.status_code,
            message=exc.message
        ),
    )

@app.get("/health-check", response_model=BaseResponse)
def health_check() -> JSONResponse:
    return api_response(
        status_code=ResponsesEnum.HEALTH_CHECK_OK.status_code,
        response=BaseResponse(
            status_code=ResponsesEnum.HEALTH_CHECK_OK.status_code,
            message=ResponsesEnum.HEALTH_CHECK_OK.message
        )
    )

