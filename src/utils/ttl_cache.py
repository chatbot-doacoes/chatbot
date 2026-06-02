from datetime import datetime, timedelta
from typing import Any


class TTLCache:
    def __init__(self, ttl_seconds: int) -> None:
        self._ttl_seconds = ttl_seconds
        self._expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache = {}

    def set(self, key: str, value: Any) -> None:
        self._cache[key] = value
        self._expires_at = datetime.now() + timedelta(seconds=self._ttl_seconds)

    def get(self, key: str) -> str | None:
        if self.is_expired():
            self._cache.clear()
            return None
        return self._cache.get(key)

    def is_empty(self) -> bool:
        return not bool(self._cache)

    def is_expired(self) -> bool:
        return datetime.now() > self._expires_at