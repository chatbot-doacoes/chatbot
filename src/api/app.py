from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from src.api.base_response import BaseResponse
from src.api.middlewares.ip_allowlist import set_ip_allowlist
from src.api.public.router import public_router
from src.api.internal.router import internal_router
from src.api.exceptions import APIException
from src.utils.utils import api_response


app = FastAPI(title="Chatbot API")
set_ip_allowlist(app)

app.include_router(internal_router, include_in_schema=False)
app.include_router(public_router)

@app.exception_handler(APIException)
def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return api_response(
        status_code=exc.status_code,
        message=exc.message,
    )

@app.get("/health-check", response_model=BaseResponse)
def health_check() -> BaseResponse:
    return BaseResponse(
        status_code=status.HTTP_200_OK,
        message="The service is healthy!"
    )

