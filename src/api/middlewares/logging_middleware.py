from fastapi import FastAPI, Request
from time import perf_counter
import uuid

from src.utils.logger import Logger
from src.enum.status_enum import StatusEnum

logger = Logger()

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

        log_data = logger.create_log(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        logger.add_step(log_data, "Request started")

        try:

            response = await call_next(request)

            duration = perf_counter() - start_time

            logger.add_step(log_data, "Request finished")

            logger.add_metadata(
                log_data,
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            if response.status_code >= 400:
                logger.set_status(log_data, StatusEnum.ERROR)
            else:
                logger.set_status(log_data, StatusEnum.SUCCESS)

            logger.generate_log(log_data)

            return response

        except Exception:

            logger.add_step(
                log_data,
                "Unhandled internal exception"
            )

            logger.set_status(
                log_data,
                StatusEnum.ERROR
            )

            logger.generate_log(log_data)

            raise