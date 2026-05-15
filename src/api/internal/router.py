from fastapi import APIRouter, Depends
from src.api.dependencies.validations import verify_internal_api_key
from src.api.internal.endpoints import institutions

internal_router = APIRouter(
    prefix="/internal",
    dependencies=[Depends(verify_internal_api_key)],
)

internal_router.include_router(institutions.router, tags=["Institutions"])