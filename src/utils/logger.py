import json
import logging
from typing import TypedDict, List, Dict, Any

from src.enum.StatusEnum import StatusEnum

class LogData(TypedDict):
    status: str
    steps: List[str]
    metadata: Dict[str, Any]

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self._reset_state()

    def _reset_state(self) -> None:
        self.final_log: LogData = {
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
