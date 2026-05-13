from supabase import Client, create_client
from src.utils.logger import Logger
from src.config.environment import Environment
from src.utils.ttl_cache import TTLCache

INSTITUTIONS_TABLE = "institutions"
KEY_HASH_COLUMN = "key_hash"
KEY_HASHES_LIST = "key_hashes_list"

key_hashes_cache = TTLCache(ttl_seconds=300) # 5 Minutes

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

    def register_institution(self, data: dict) -> bool:
        return self._create_record(
            table_name=INSTITUTIONS_TABLE,
            data=data,
        )

    def is_institution_registered(self, key_hash: str) -> bool:
        key_hashes_list = key_hashes_cache.get(KEY_HASHES_LIST)
        if key_hashes_list is not None:
            return key_hash in key_hashes_list

        try:
            self.logger.add_step("Trying to get key hashes from Supabase.")
            response = (
                self.client.table(INSTITUTIONS_TABLE)
                .select(KEY_HASH_COLUMN)
                .execute()
            )
            data = getattr(response, "data", None)
            if not data or not isinstance(data, list):
                return False

            key_hashes_list = [row[KEY_HASH_COLUMN] for row in data]
            key_hashes_cache.set(KEY_HASHES_LIST, key_hashes_list)
            return key_hash in key_hashes_list
        except Exception as e:
            self.logger.add_step(f"Failed to get key hashes from Supabase: {str(e)}")
            return False
