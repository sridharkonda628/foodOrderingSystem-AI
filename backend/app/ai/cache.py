import time
import hashlib
from typing import Any, Optional, Dict, Tuple


class QueryCache:
    def __init__(self, default_ttl_seconds: int = 300):
        self._cache: Dict[str, Tuple[float, Any]] = {}
        self.default_ttl = default_ttl_seconds

    @staticmethod
    def normalize_key(query: str) -> str:
        cleaned = " ".join(query.lower().strip().split())
        return hashlib.sha256(cleaned.encode("utf-8")).hexdigest()

    def get(self, query: str) -> Optional[Any]:
        key = self.normalize_key(query)
        if key in self._cache:
            expires_at, data = self._cache[key]
            if time.time() < expires_at:
                return data
            else:
                del self._cache[key]
        return None

    def set(self, query: str, data: Any, ttl_seconds: Optional[int] = None) -> None:
        key = self.normalize_key(query)
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        self._cache[key] = (time.time() + ttl, data)

    def clear(self) -> None:
        self._cache.clear()


search_cache = QueryCache(default_ttl_seconds=300)
