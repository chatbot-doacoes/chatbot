from fastapi import FastAPI, HTTPException, Request, status

from src.config.environment import Environment

ALLOWED_IPS_ENV_NAME = "ALLOWED_IPS"

def set_ip_allowlist(app: FastAPI) -> None:
    @app.middleware("http")
    async def ip_allowlist_middleware(request: Request, call_next):
        allowed_ips_raw = Environment.get(ALLOWED_IPS_ENV_NAME)
        if not allowed_ips_raw:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{ALLOWED_IPS_ENV_NAME} is not configured",
            )

        allowed_ips = {item.strip() for item in allowed_ips_raw.split(",") if item.strip()}
        if not allowed_ips:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"{ALLOWED_IPS_ENV_NAME} is empty",
            )

        client_info = request.client
        client_ip = client_info.host if client_info else ""
        if not client_ip or client_ip not in allowed_ips:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="IP not allowed",
            )
        return await call_next(request)
