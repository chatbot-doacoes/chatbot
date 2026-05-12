from fastapi import Depends, FastAPI

from src.api.dependencies.validations import verify_api_key
from src.api.middlewares.ip_allowlist import set_ip_allowlist
from src.api.payloads.messages import MessagesPayload

app = FastAPI(title="Chatbot API")
set_ip_allowlist(app)

@app.post("/messages")
def send_messages(payload: MessagesPayload, _: None = Depends(verify_api_key)) -> dict:
    return {"status": "ok", "message": payload.message}
