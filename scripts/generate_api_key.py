import secrets
from src.utils.utils import hash_api_key

# WARNING: This functions is only to internal use.
def generate_external_api_key():
    random_value = secrets.token_urlsafe(32)
    print(f"institution_sk_{random_value}")

def generate_internal_api_key():
    random_value = secrets.token_urlsafe(32)
    api_key = f"internal_sk_{random_value}"
    print(api_key)
    print(hash_api_key(api_key))

if __name__ == "__main__":
    generate_external_api_key()
    generate_internal_api_key()