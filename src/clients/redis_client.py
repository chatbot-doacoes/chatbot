import json

from src.utils.logger import Logger
import redis
import os

class Redis:

    client_instance = None

    def __init__(self, logger: Logger):
        self.logger = logger
        if Redis.client_instance is None:
            # Validar com o Victor como será feita a conexão
            # redis.Redis.from_url(os.getenv("REDIS_URL"))
            Redis.client_instance = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                username=os.getenv("REDIS_USERNAME"),
                password=os.getenv("REDIS_PASSWORD"),
                decode_responses=True
            )

        self.client = Redis.client_instance
        try:
            self.logger.add_step("Trying to connect to Redis.")
            self.client.ping()
        except redis.ConnectionError as e:
            self.logger.add_step(f"Error to connect to Redis: {str(e)}")

    def close_connection(self) -> None:
        if self.client:
            self.logger.add_step("Closing Redis connection.")
            self.client.close()

    def get_queue_message(self, queue_name: str) -> dict:
        try:
            self.logger.add_step("Trying to get message from Redis queue.")
            result = self.client.blpop(queue_name, timeout=0)
            return json.loads(result[1])
        except redis.RedisError as e:
            self.logger.add_step(f"Error to get message to Redis queue: {str(e)}")
            return {}
