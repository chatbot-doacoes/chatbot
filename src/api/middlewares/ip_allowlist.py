from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse

from src.config.environment import Environment
from src.utils.utils import api_response

ALLOWED_IPS_ENV_NAME = "ALLOWED_IPS"

def set_ip_allowlist(app: FastAPI) -> None:
    @app.middleware("http")
    async def ip_allowlist_middleware(request: Request, call_next) -> JSONResponse:
        allowed_ips_raw = Environment.get(ALLOWED_IPS_ENV_NAME)
        allowed_ips = {item.strip() for item in (allowed_ips_raw or "").split(",") if item.strip()}

        client_info = request.client
        client_ip = client_info.host if client_info else None

        if client_ip not in allowed_ips:
            return api_response(
                status_code=status.HTTP_403_FORBIDDEN,
                message="IP not allowed",
            )
        return await call_next(request)
