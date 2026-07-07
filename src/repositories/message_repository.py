from uuid import UUID
from src.models.message import MessageModel
from src.clients.supabase_client import SupabaseClient

class MessageRepository:
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase_client = supabase_client

    def register(self, model: MessageModel) -> bool:
        return self.supabase_client.create_record(
            table_name=MessageModel.TABLE_NAME,
            data=model.to_insert_dict(),
        )

    def get_templates_by_institution(self, institution_id: str | UUID) -> list[dict[str, str]]:
        if not institution_id:
            return []
        try:
            self.supabase_client.logger.add_step(f"Trying to get messages templates for institution '{institution_id}'.")
            response = (
                self.supabase_client.client.table(MessageModel.TABLE_NAME)
                .select(
                    MessageModel.Cols.tag,
                    MessageModel.Cols.message_template
                )
                .eq(MessageModel.Cols.institution_id, str(institution_id))
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return []
            return data
        except Exception as e:
            self.supabase_client.logger.add_step(f"Failed to get messages templates for institution '{institution_id}': {str(e)}")
            return []

    def get_by_institution(self, institution_id: UUID | str) -> list[MessageModel]:
        try:
            self.supabase_client.logger.add_step(f"Trying to get messages for institution '{institution_id}'.")
            response = (
                self.supabase_client.client.table(MessageModel.TABLE_NAME)
                .select("*")
                .eq(MessageModel.Cols.institution_id, str(institution_id))
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return []
            return [MessageModel.model_validate(row) for row in data]
        except Exception as e:
            self.supabase_client.logger.add_step(f"Failed to get messages for institution '{institution_id}': {str(e)}")
            raise
