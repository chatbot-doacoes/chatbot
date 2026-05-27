from supabase import Client, create_client
from uuid import UUID
from src.utils.logger import Logger
from src.config.environment import Environment
from src.utils.ttl_cache import TTLCache
from src.models.institution import InstitutionModel
from src.models.message import MessageModel


key_hashes_cache = TTLCache(ttl_seconds=300)
KEY_HASHES_LIST = "key_hashes_list"


class Supabase:
    def __init__(self, logger: Logger):
        self.logger = logger
        try:
            self.client: Client = create_client(
                supabase_url=Environment.get("SUPABASE_URL"),
                supabase_key=Environment.get("SUPABASE_SECRET_API_KEY")
            )
        except Exception as e:
            self.logger.add_step(f"Failed to create Supabase client: {str(e)}")

    def _create_record(self, table_name: str, data: dict) -> bool:
        try:
            response = self.client.table(table_name).insert(data).execute()
            return bool(getattr(response, "data", None))
        except Exception as e:
            self.logger.add_step(f"Failed to create record in {table_name}: {str(e)}")
            return False

    def register_institution(self, model: InstitutionModel) -> bool:
        return self._create_record(
            table_name=InstitutionModel.TABLE_NAME,
            data=model.to_insert_dict(),
        )

    def register_message(self, model: MessageModel) -> bool:
        return self._create_record(
            table_name=MessageModel.TABLE_NAME,
            data=model.to_insert_dict(),
        )

    def is_institution_registered(self, key_hash: str) -> bool:
        key_hashes_list = key_hashes_cache.get(KEY_HASHES_LIST)
        if key_hashes_list is not None:
            return key_hash in key_hashes_list

        try:
            response = (
                self.client.table(InstitutionModel.TABLE_NAME)
                .select("*")
                .eq(InstitutionModel.Cols.is_active, True)
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return False

            institutions = [InstitutionModel.model_validate(row) for row in data]
            key_hashes_list = [inst.key_hash for inst in institutions]
            key_hashes_cache.set(KEY_HASHES_LIST, key_hashes_list)
            
            return key_hash in key_hashes_list
        except Exception as e:
            self.logger.add_step(f"Failed to check institution registration: {str(e)}")
            return False
        
    def get_messages_by_institution(self, institution_id: UUID | str) -> list[MessageModel]:
        try:
            self.logger.add_step(f"Trying to get messages for institution '{institution_id}'.")
            response = (
                self.client.table(MessageModel.TABLE_NAME)
                .select("*")
                .eq(MessageModel.Cols.institution_id, str(institution_id))
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return []

            return [MessageModel.model_validate(row) for row in data]
        except Exception as e:
            self.logger.add_step(f"Failed to get messages for institution '{institution_id}': {str(e)}")
            return []
        
    def get_institutions(self) -> list[InstitutionModel]:
        self.logger.add_step("Trying to get institutions from Supabase.")
        response = (
            self.client.table(InstitutionModel.TABLE_NAME)
            .select("*")
            .execute()
        )
        data = getattr(response, "data", None)
        if not data or not isinstance(data, list):
            return []
        return [InstitutionModel.model_validate(row) for row in data]
    
    def update_institution(self, institution_id: str, data: dict) -> InstitutionModel:
        self.logger.add_step(f"Trying to update institution '{institution_id}'.")
        response = (
            self.client.table(InstitutionModel.TABLE_NAME)
            .update(data)
            .eq(InstitutionModel.Cols.id, institution_id)
            .execute()
        )
        result = getattr(response, "data", None)
        if not result or not isinstance(result, list):
            raise Exception(f"Institution '{institution_id}' not found")
        return InstitutionModel.model_validate(result[0])
