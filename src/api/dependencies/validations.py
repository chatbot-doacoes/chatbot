from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

from src.clients.supabase_client import Supabase
from src.utils.utils import hash_api_key

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)


class ValidationsDependencies:
    def __init__(self, supabase: Supabase):
        self._supabase = supabase

    def verify_api_key(self, api_key: str | None = Depends(api_key_header)) -> None:
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="API Key is missing",
            )

        if not self._supabase.is_institution_registered(
            key_hash=hash_api_key(api_key),
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This API Key is not registered",
            )
