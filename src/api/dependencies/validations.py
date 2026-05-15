from fastapi import status, Security
from fastapi.security import APIKeyHeader

from src.api.exceptions import APIException
from src.clients.supabase_client import Supabase
from src.config.environment import Environment
from src.utils.logger import Logger
from src.utils.utils import hash_api_key


external_api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)
internal_api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

def verify_external_api_key(api_key: str | None = Security(external_api_key_header)):
    # Revisar esse fluxo de logs...
    logger = Logger()
    supabase_client = Supabase(logger)

    if not api_key:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="API Key is missing",
        )

    if not supabase_client.is_institution_registered(
        key_hash=hash_api_key(api_key),
    ):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="This API Key is not registered",
        )

def verify_internal_api_key(api_key: str | None = Security(internal_api_key_header)):
    if not api_key:
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="API Key is missing",
        )

    if hash_api_key(api_key) != Environment.get("INTERNAL_API_KEY"):
        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="This API Key is not registered",
        )
