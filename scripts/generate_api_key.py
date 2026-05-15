import secrets

# WARNING: This function is only to internal use.
def generate_api_key() -> str:
    random_value = secrets.token_urlsafe(32)
    return f"institution_sk_{random_value}"

if __name__ == "__main__":
    print(generate_api_key())