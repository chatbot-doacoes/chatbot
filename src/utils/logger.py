import json
import logging
from datetime import datetime, timezone


class Logger:

    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s"
        )

        self.logger = logging.getLogger(__name__)

    def create_log(
        self,
        request_id: str,
        method: str,
        path: str
    ) -> dict:

        return {
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "",
            "steps": [],
            "metadata": {
                "method": method,
                "path": path,
            }
        }

    def add_step(
        self,
        log_data: dict,
        step: str
    ) -> None:

        log_data["steps"].append(step)

    def add_metadata(
        self,
        log_data: dict,
        **data
    ) -> None:

        log_data["metadata"].update(data)

    def set_status(
        self,
        log_data: dict,
        status: str
    ) -> None:

        log_data["status"] = status

    def generate_log(
        self,
        log_data: dict
    ) -> None:

        self.logger.info(json.dumps(log_data))