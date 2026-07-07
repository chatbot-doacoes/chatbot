from supabase import Client, create_client
from src.utils.logger import Logger
from src.config.environment import Environment

class SupabaseClient:
    def __init__(self, logger: Logger):
        self.logger = logger
        try:
            self.client: Client = create_client(
                supabase_url=Environment.get("SUPABASE_URL"),
                supabase_key=Environment.get("SUPABASE_SECRET_API_KEY")
            )
        except Exception as e:
            self.logger.add_step(f"Failed to create Supabase client: {str(e)}")

    def create_record(self, table_name: str, data: dict) -> bool:
        try:
            response = self.client.table(table_name).insert(data).execute()
            result = getattr(response, "data", None)
            return bool(result)
        except Exception as e:
            self.logger.add_step(
                f"Failed to create record in {table_name}: {str(e)}"
            )
            return False
