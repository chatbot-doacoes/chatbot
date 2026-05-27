from fastapi import status, Security, Request
from fastapi.security import APIKeyHeader

from src.api.exceptions import APIException
from src.clients.supabase_client import Supabase
from src.config.environment import Environment
from src.utils.utils import hash_api_key

INTERNAL_API_KEY = "INTERNAL_API_KEY"

external_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
internal_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False) #auto_error falso para permitir tratamento customizado do erro no log


def verify_external_api_key(
    request: Request,
    api_key: str | None = Security(external_api_key_header)
) -> None:

    logger = request.state.logger

    logger.add_step("Validating external API key")

    supabase_client = Supabase(logger)

    if not api_key:

        logger.add_step("External API key is missing")

        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="API Key is missing",
        )

    if not supabase_client.is_institution_registered(
        key_hash=hash_api_key(api_key),
    ):

        logger.add_step("External API key is not registered")

        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="This API Key is not registered",
        )

    logger.add_step("External API key validated successfully")


def verify_internal_api_key(
    request: Request,
    api_key: str | None = Security(internal_api_key_header)
) -> None:

    logger = request.state.logger

    logger.add_step("Validating internal API key")

    if not api_key:

        logger.add_step("Internal API key is missing")

        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="API Key is missing",
        )

    if hash_api_key(api_key) != Environment.get(INTERNAL_API_KEY):

        logger.add_step("Internal API key is not registered")

        raise APIException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="This API Key is not registered",
        )

    logger.add_step("Internal API key validated successfully")