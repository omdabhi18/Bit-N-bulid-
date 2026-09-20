import json
import time
from typing import Optional, Any
from app.config import settings
from app.utils.logger import logger

class MemoryCacheFallback:
    def __init__(self):
        self._store = {}

    def get(self, key: str) -> Optional[str]:
        if key in self._store:
            val, expiry = self._store[key]
            if expiry is None or expiry > time.time():
                return val
            else:
                del self._store[key]
        return None

    def set(self, key: str, val: str, ttl: Optional[int] = None):
        expiry = (time.time() + ttl) if ttl else None
        self._store[key] = (val, expiry)

    def delete(self, key: str):
        self._store.pop(key, None)

class CacheService:
    def __init__(self):
        self._redis = None
        self._memory = MemoryCacheFallback()
        self._use_redis = False
        self._init_redis()

    def _init_redis(self):
        try:
            import redis
            self._redis = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=1.0)
            self._redis.ping()
            self._use_redis = True
            logger.info(f"Connected to Redis cache at {settings.REDIS_URL}")
        except Exception as e:
            logger.info(f"Redis not available ({e}). Using in-memory TTL cache fallback.")
            self._use_redis = False

    async def get(self, key: str) -> Optional[Any]:
        try:
            if self._use_redis and self._redis:
                val = self._redis.get(key)
                if val:
                    return json.loads(val)
        except Exception as e:
            logger.warning(f"Redis GET failed for {key}: {e}. Falling back to memory.")
            self._use_redis = False

        mem_val = self._memory.get(key)
        return json.loads(mem_val) if mem_val else None

    async def set(self, key: str, value: Any, ttl_seconds: int = 1800) -> bool:
        serialized = json.dumps(value)
        self._memory.set(key, serialized, ttl_seconds)
        try:
            if self._use_redis and self._redis:
                self._redis.setex(key, ttl_seconds, serialized)
                return True
        except Exception as e:
            logger.warning(f"Redis SET failed for {key}: {e}. Memory cache retained.")
            self._use_redis = False
        return True

    async def get_json(self, key: str) -> Optional[Any]:
        return await self.get(key)

    async def set_json(self, key: str, value: Any, expire_seconds: int = 1800) -> bool:
        return await self.set(key, value, ttl_seconds=expire_seconds)

    async def delete(self, key: str):
        self._memory.delete(key)
        try:
            if self._use_redis and self._redis:
                self._redis.delete(key)
        except Exception:
            pass

cache_service = CacheService()
