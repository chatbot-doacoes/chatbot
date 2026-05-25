from supabase import Client, create_client
from src.utils.logger import Logger
from src.config.environment import Environment
from src.utils.ttl_cache import TTLCache
from src.models.institution import InstitutionModel


key_hashes_cache = TTLCache(ttl_seconds=300)
KEY_HASHES_LIST = "key_hashes_list"


class Supabase:
    def __init__(self, logger: Logger):
        self.logger = logger
        try:
            self.logger.add_step("Trying to connect to Supabase.")
            self.client: Client = create_client(
                supabase_url=Environment.get("SUPABASE_URL"),
                supabase_key=Environment.get("SUPABASE_SECRET_API_KEY")
            )
        except Exception as e:
            self.logger.add_step(f"Failed to create Supabase client: {str(e)}")

    def _create_record(self, table_name: str, data: dict) -> bool:
        try:
            self.logger.add_step(f"Trying to insert record into '{table_name}'.")
            response = self.client.table(table_name).insert(data).execute()
            return bool(getattr(response, "data", None))
        except Exception as e:
            self.logger.add_step(f"Failed to insert record into '{table_name}': {str(e)}")
            return False

    def register_institution(self, model: InstitutionModel) -> bool:
        return self._create_record(
            table_name=InstitutionModel.TABLE_NAME,
            data=model.to_insert_dict(),
        )

    def is_institution_registered(self, key_hash: str) -> bool:
        key_hashes_list = key_hashes_cache.get(KEY_HASHES_LIST)
        if key_hashes_list is not None:
            return key_hash in key_hashes_list

        try:
            self.logger.add_step("Trying to get key hashes from Supabase.")
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
            self.logger.add_step(f"Failed to get key hashes from Supabase: {str(e)}")
            return False
        
    def get_institutions(self) -> list:
        try:
            self.logger.add_step("Trying to get institutions from Supabase.")
            response = (
                self.client.table(InstitutionModel.TABLE_NAME)
                .select("id, institution_name, is_active, created_at, update_at")
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return []
            return data
        except Exception as e:
            self.logger.add_step(f"Failed to get institutions: {str(e)}")
            return []
