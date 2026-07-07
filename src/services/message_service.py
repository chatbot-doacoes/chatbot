from uuid import UUID
from src.repositories.message_repository import MessageRepository
from src.models.message import MessageModel
from src.api.internal.payloads.messages import RegisterMessage

class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def register_message(self, institution_id: UUID, payload: RegisterMessage) -> bool:
        message_model = MessageModel(
            institution_id=institution_id,
            tag=payload.tag,
            message_template=payload.message_template
        )
        return self.repository.register(message_model)

    def get_messages_by_institution(self, institution_id: UUID) -> list[MessageModel]:
        return self.repository.get_by_institution(institution_id)
        
    def get_messages_templates(self, institution_id: str | UUID) -> list[dict[str, str]]:
        return self.repository.get_templates_by_institution(institution_id)
