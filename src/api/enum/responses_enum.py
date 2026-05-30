from enum import Enum
from fastapi import status


class ResponsesEnum(Enum):
    # --- Success Responses (2xx) ---
    HEALTH_CHECK_OK = (status.HTTP_200_OK, "The service is healthy!")
    INSTITUTIONS_FETCHED = (status.HTTP_200_OK, "Successfully fetched institutions.")
    INSTITUTION_CREATED = (status.HTTP_201_CREATED, "Institution created successfully.")
    INSTITUTION_UPDATED = (status.HTTP_200_OK, "Institution updated successfully.")

    # --- Error Responses (4xx) ---
    IP_NOT_ALLOWED = (status.HTTP_403_FORBIDDEN, "IP not allowed.")
    API_KEY_MISSING = (status.HTTP_401_UNAUTHORIZED, "API Key is missing.")
    API_KEY_INVALID = (status.HTTP_401_UNAUTHORIZED, "This API Key is not registered.")
    NO_FIELDS_TO_UPDATE = (status.HTTP_400_BAD_REQUEST, "No fields to update.")
    INVALID_FIELDS = (status.HTTP_422_UNPROCESSABLE_ENTITY, "The request body has invalid fields.")

    # --- Server Error Responses (5xx) ---
    FAILED_TO_FETCH_INSTITUTIONS = (status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch institutions.")
    FAILED_TO_UPDATE_INSTITUTION = (status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update institution.")

    def __init__(self, status_code: int, message: str):
        self._status_code = status_code
        self._message = message

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def message(self) -> str:
        return self._message