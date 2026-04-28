from src.utils.logger import Logger
from src.clients.twilio_client import Twilio
from src.clients.redis_client import Redis

if __name__ == "__main__":
    logger = Logger()
    twilio_client = Twilio(logger=logger)
    redis_client = Redis(logger=logger)

    twilio_client.send_whatsapp_message(
        to_number="999999999999",
        message="Teste API Twilio."
    )