import json
import logging
from datetime import datetime, timezone


class Logger:

    def __init__(
        self,
        request_id: str,
        method: str,
        path: str
    ):

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s"
        )

        self.logger = logging.getLogger(__name__)

        self.log_data = {
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
        step: str
    ) -> None:

        self.log_data["steps"].append(step)

    def add_metadata(
        self,
        **data
    ) -> None:

        self.log_data["metadata"].update(data)

    def set_status(
        self,
        status: str
    ) -> None:

        self.log_data["status"] = status

    def generate_log(self) -> None:

        self.logger.info(json.dumps(self.log_data))