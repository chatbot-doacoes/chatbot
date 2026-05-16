import json
import logging


class Logger:

    def __init__(self):

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s"
        )

        self.logger = logging.getLogger(__name__)

    def generate_log(self, log_data: dict) -> None:

        self.logger.info(json.dumps(log_data))