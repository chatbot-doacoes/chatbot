from fastapi import APIRouter, Depends
from src.api.dependencies.validations import verify_internal_api_key
from src.api.internal.endpoints import institutions, messages, user

internal_router = APIRouter(
    prefix="/internal",
    dependencies=[Depends(verify_internal_api_key)],
)

internal_router.include_router(institutions.router, tags=["Institutions"])
internal_router.include_router(messages.router, tags=["Messages"])
internal_router.include_router(user.router, tags=["User"])