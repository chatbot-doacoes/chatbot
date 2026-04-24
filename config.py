from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # --- Twilio ---
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_WHATSAPP_NUMBER: str   # Ex: +14155238886 (sandbox) ou seu número aprovado
    TWILIO_CONTENT_SID: str       # Ex: HXb5b62575e6e4ff6129ad7c8efe1f983e

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379"
    REDIS_CHANNEL: str = "campanhas_doacao"

    # --- API externa de doadores (Opção B - preencher quando disponível) ---
    DONORS_API_URL: str = ""
    DONORS_API_TOKEN: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
print(settings.TWILIO_ACCOUNT_SID)
