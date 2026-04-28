import os
from dotenv import load_dotenv

class Environment:
    load_dotenv()

    @staticmethod
    def get(name: str, default=None) -> str:
        return os.getenv(name, default)
