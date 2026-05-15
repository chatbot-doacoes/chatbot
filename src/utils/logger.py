import json
import logging
from typing import TypedDict, List, Dict, Any
from datetime import datetime, timezone

from src.enum.status_enum import StatusEnum

class LogData(TypedDict):
    request_id: str
    timestamp: str
    status: str
    steps: List[str]
    metadata: Dict[str, Any]

class Logger:
    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s"
        )

        self.logger = logging.getLogger(__name__)

        self._reset_state()

    def _reset_state(self) -> None:
        self.final_log: LogData = {
            "request_id": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "",
            "steps": [],
            "metadata": {}
        }

    def add_step(self, step: str) -> None:
        self.final_log["steps"].append(step)

    def add_to_final_log(self, **data) -> None:
        self.final_log["metadata"].update(data)

    def generate_log(self, status: StatusEnum) -> None:
        self.final_log["status"] = status
        self.logger.info(json.dumps(self.final_log))
        self._reset_state()

    def set_request_id(self, request_id: str) -> None:
        self.final_log["request_id"] = request_id
