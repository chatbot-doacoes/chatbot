from fastapi import FastAPI, Request
from time import perf_counter

from src.utils.logger import Logger
from src.enum.status_enum import StatusEnum

logger = Logger()


def set_logging_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):

        start_time = perf_counter()

        request_id = getattr(request.state, "request_id", "")

        logger.set_request_id(request_id)

        logger.add_step("Request started")

        logger.add_to_final_log(
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)

            duration = perf_counter() - start_time

            logger.add_step("Request finished")

            logger.add_to_final_log(
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            logger.generate_log(StatusEnum.SUCCESS)

            return response

        except Exception as e:

            logger.add_step(f"Unhandled exception: {str(e)}")

            logger.generate_log(StatusEnum.ERROR)

            raise