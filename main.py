import asyncio
import logging
from redis_consumer import RedisConsumer
from whatsapp_service import WhatsAppService
from donor_service import DonorService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🤖 Chatbot de doações iniciando...")

    whatsapp = WhatsAppService()
    donor_service = DonorService()
    consumer = RedisConsumer(whatsapp, donor_service)

    await consumer.start()


if __name__ == "__main__":
    asyncio.run(main())
