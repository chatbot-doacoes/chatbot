import uuid

from fastapi import FastAPI, Request


def set_request_context(app: FastAPI) -> None:

    @app.middleware("http")
    async def request_context_middleware(
        request: Request,
        call_next
    ):

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        response = await call_next(request)

        return response