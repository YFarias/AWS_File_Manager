from __future__ import annotations


class RedisClient:
    """Placeholder for future rate-limiting and caching support."""

    def __init__(self, redis_url: str | None = None) -> None:
        self.redis_url = redis_url

    async def is_rate_limited(self, key: str, limit: int, window_seconds: int) -> bool:
        _ = (key, limit, window_seconds)
        return False
