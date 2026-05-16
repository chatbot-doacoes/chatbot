from fastapi import Depends, FastAPI

from src.api.dependencies.validations import ValidationsDependencies
from src.api.middlewares.ip_allowlist import set_ip_allowlist
from src.api.middlewares.request_context import set_request_context
from src.api.middlewares.logging_middleware import set_logging_middleware
from src.api.payloads.messages import MessagesPayload
from src.clients.supabase_client import Supabase
from src.utils.logger import Logger

import time

app = FastAPI(title="Chatbot API")
set_logging_middleware(app)
set_request_context(app)
set_ip_allowlist(app)

logger = Logger()

supabase_client = Supabase(logger=logger)

validation_dependencies = ValidationsDependencies(
    supabase=supabase_client,
)

@app.post("/send-messages")
def send_messages(
        payload: MessagesPayload,
        _: None = Depends(validation_dependencies.verify_api_key)) -> dict:
    return {"status": "ok", "message": payload.message}

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA CADASTRAR NOVAS INSTITUIÇÕES

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA RETORNAR TODAS AS INSTITUIÇÕES CADASTRADAS

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA DELEÇÃO DE INSTITUIÇÕES CADASTRADAS

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA CRIAÇÃO DE NOVAS MENSAGENS

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA RETORNAR TODAS AS MENSAGENS

# IMPLEMENTAR ENDPOINT DE USO INTERNO PARA DELEÇÃO DE MENSAGENS

# (OPCIONAL) IMPLEMENTAR ENDPOINT PARA ALTERAÇÃO DE MENSAGENS E INSTITUIÇÕES