from fastapi import Request
from src.clients.supabase_client import SupabaseClient
from src.repositories.institution_repository import InstitutionRepository
from src.repositories.message_repository import MessageRepository
from src.services.institution_service import InstitutionService
from src.services.message_service import MessageService

def get_supabase_client(request: Request) -> SupabaseClient:
    return SupabaseClient(request.state.logger)

def get_institution_repository(request: Request) -> InstitutionRepository:
    client = get_supabase_client(request)
    return InstitutionRepository(client)

def get_message_repository(request: Request) -> MessageRepository:
    client = get_supabase_client(request)
    return MessageRepository(client)

def get_institution_service(request: Request) -> InstitutionService:
    repo = get_institution_repository(request)
    return InstitutionService(repo)

def get_message_service(request: Request) -> MessageService:
    repo = get_message_repository(request)
    return MessageService(repo)
