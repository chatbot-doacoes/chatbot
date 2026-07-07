from fastapi import status, Security, Request, Depends
from fastapi.security import APIKeyHeader

from src.api.enum.responses_enum import ResponsesEnum
from src.api.exceptions import APIException
from src.services.institution_service import InstitutionService
from src.api.dependencies.core import get_institution_service
from src.config.environment import Environment
from src.utils.utils import hash_api_key

INTERNAL_API_KEY = "INTERNAL_API_KEY"

external_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
internal_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False) 

def verify_external_api_key(
    request: Request,
    api_key: str | None = Security(external_api_key_header),
    institution_service: InstitutionService = Depends(get_institution_service)
) -> None:

    logger = request.state.logger
    logger.add_step("Validating external API key")

    if not api_key:
        logger.add_step("External API key is missing")
        raise APIException(
            status_code=ResponsesEnum.API_KEY_MISSING.status_code,
            message=ResponsesEnum.API_KEY_MISSING.message,
        )

    if not institution_service.is_institution_registered(
        key_hash=hash_api_key(api_key),
    ):
        logger.add_step("External API key is not registered")
        raise APIException(
            status_code=ResponsesEnum.API_KEY_INVALID.status_code,
            message=ResponsesEnum.API_KEY_INVALID.message,
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
            status_code=ResponsesEnum.API_KEY_MISSING.status_code,
            message=ResponsesEnum.API_KEY_MISSING.message,
        )

    if hash_api_key(api_key) != Environment.get(INTERNAL_API_KEY):
        logger.add_step("Internal API key is not registered")
        raise APIException(
            status_code=ResponsesEnum.API_KEY_INVALID.status_code,
            message=ResponsesEnum.API_KEY_INVALID.message,
        )

    logger.add_step("Internal API key validated successfully")