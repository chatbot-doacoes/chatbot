from twilio.rest import Client
from src.utils.logger import Logger
from src.config.environment import Environment

class Twilio:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.from_number = self._format_whatsapp_number(Environment.get("TWILIO_WHATSAPP_FROM"))
        try:
            self.client = Client(
                username=Environment.get("TWILIO_ACCOUNT_SID"),
                password=Environment.get("TWILIO_AUTH_TOKEN"),
            )
        except Exception as e:
            self.logger.add_step(f"Failed to create Twilio client: {str(e)}")

    @staticmethod
    def _format_whatsapp_number(raw_number: str) -> str:
        return f"whatsapp:+{raw_number}"

    def send_whatsapp_message(self, to_number: str, message: str):
        try:
            self.client.messages.create(
                from_=self.from_number,
                to=self._format_whatsapp_number(to_number),
                body=message,
            )
        except Exception as e:
            self.logger.add_step(f"Failed to send WhatsApp message: {str(e)}")
