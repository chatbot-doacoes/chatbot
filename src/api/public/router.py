from fastapi import APIRouter, Depends
from src.api.dependencies.validations import verify_external_api_key
from src.api.public.endpoints import messages

public_router = APIRouter(
    prefix="/api/v1"
)

public_router.include_router(messages.router, tags=["Messages"])