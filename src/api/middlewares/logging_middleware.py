from fastapi import FastAPI, Request
from time import perf_counter
import uuid

from src.utils.logger import Logger
from src.enum.status_enum import StatusEnum


# Middleware responsável por gerar logs estruturados e centralizados
# para cada request da API. Registra request_id, método HTTP, endpoint,
# tempo de resposta, status da requisição e exceções não tratadas,
# garantindo rastreabilidade e observabilidade do sistema.

def set_logging_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):

        start_time = perf_counter()

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        logger = Logger(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        # Armazena a instância do logger da request atual para permitir
        # enriquecimento dos logs em outras camadas da aplicação.
        request.state.logger = logger

        logger.add_step("Request started")

        try:

            response = await call_next(request)

            duration = perf_counter() - start_time

            logger.add_step("Request finished")

            logger.add_metadata(
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            if response.status_code >= 400:
                logger.set_status(StatusEnum.ERROR)
            else:
                logger.set_status(StatusEnum.SUCCESS)

            logger.generate_log()

            return response

        except Exception:

            logger.add_step(
                "Unhandled internal exception"
            )

            logger.set_status(
                StatusEnum.ERROR
            )

            logger.generate_log()

            raise