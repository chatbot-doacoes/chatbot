from fastapi import FastAPI, Request
from time import perf_counter
from datetime import datetime, timezone
import traceback

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

        request_id = getattr(request.state, "request_id", "")

        log_data = {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "",
            "steps": [],
            "metadata": {
                "method": request.method,
                "path": request.url.path,
            }
        }

        log_data["steps"].append("Request started")

        try:

            response = await call_next(request)

            duration = perf_counter() - start_time

            log_data["steps"].append("Request finished")

            log_data["metadata"]["status_code"] = response.status_code

            log_data["metadata"]["duration_ms"] = round(duration * 1000, 2)

            if response.status_code >= 400:
                log_data["status"] = StatusEnum.ERROR
            else:
                log_data["status"] = StatusEnum.SUCCESS

            logger.generate_log(log_data)

            return response

        except Exception as e:

            log_data["steps"].append(
                f"Unhandled exception: {str(e)}"
            )

            log_data["metadata"]["traceback"] = traceback.format_exc()

            log_data["status"] = StatusEnum.ERROR

            logger.generate_log(log_data)

            raise