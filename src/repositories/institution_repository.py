from datetime import datetime, timezone
from src.models.institution import InstitutionModel
from src.clients.supabase_client import SupabaseClient
from src.utils.ttl_cache import TTLCache

class InstitutionRepository:
    def __init__(self, supabase_client: SupabaseClient):
        self.supabase_client = supabase_client
        self.key_hashes_cache = TTLCache(ttl_seconds=300)
        self.KEY_HASHES_LIST = "key_hashes_list"

    def register(self, model: InstitutionModel) -> bool:
        return self.supabase_client.create_record(
            table_name=InstitutionModel.TABLE_NAME,
            data=model.to_insert_dict(),
        )

    def is_registered(self, key_hash: str) -> bool:
        key_hashes_list = self.key_hashes_cache.get(self.KEY_HASHES_LIST)
        if key_hashes_list is not None:
            return key_hash in key_hashes_list

        try:
            response = (
                self.supabase_client.client.table(InstitutionModel.TABLE_NAME)
                .select(InstitutionModel.Cols.key_hash)
                .eq(InstitutionModel.Cols.is_active, True)
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return False

            key_hashes_list = [row[InstitutionModel.Cols.key_hash] for row in data]
            self.key_hashes_cache.set(self.KEY_HASHES_LIST, key_hashes_list)
            return key_hash in key_hashes_list
        except Exception as e:
            self.supabase_client.logger.add_step(f"Failed to check institution registration: {str(e)}")
            return False

    def get_id_by_key_hash(self, key_hash: str) -> str | None:
        try:
            self.supabase_client.logger.add_step(f"Trying to get institution id by key_hash.")
            response = (
                self.supabase_client.client.table(InstitutionModel.TABLE_NAME)
                .select(InstitutionModel.Cols.id)
                .eq(InstitutionModel.Cols.key_hash, key_hash)
                .eq(InstitutionModel.Cols.is_active, True)
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return None
            return data[0][InstitutionModel.Cols.id]
        except Exception:
            self.supabase_client.logger.add_step(f"Failed to get institution id by key_hash.")
            return None

    def get_all(self) -> list[InstitutionModel]:
        self.supabase_client.logger.add_step("Trying to get institutions from Supabase.")
        response = (
            self.supabase_client.client.table(InstitutionModel.TABLE_NAME)
            .select("*")
            .execute()
        )
        data = getattr(response, "data", None)
        if not data or not isinstance(data, list):
            return []
        return [InstitutionModel.model_validate(row) for row in data]

    def update(self, institution_id: str, data: dict) -> InstitutionModel:
        self.supabase_client.logger.add_step(f"Trying to update institution '{institution_id}'.")
        data[InstitutionModel.Cols.update_at] = datetime.now(timezone.utc).isoformat()
        response = (
            self.supabase_client.client.table(InstitutionModel.TABLE_NAME)
            .update(data)
            .eq(InstitutionModel.Cols.id, institution_id)
            .execute()
        )
        result = getattr(response, "data", None)
        if not result or not isinstance(result, list):
            raise Exception(f"Institution '{institution_id}' not found")
        return InstitutionModel.model_validate(result[0])
