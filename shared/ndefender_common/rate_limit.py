from __future__ import annotations

import time
from collections import defaultdict
from dataclasses import dataclass


@dataclass
class RateLimit:
    max_per_minute: int
    window_s: int = 60


class InMemoryLimiter:
    def __init__(self) -> None:
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str, limit: RateLimit) -> bool:
        now = time.time()
        window_start = now - limit.window_s
        bucket = [ts for ts in self._buckets[key] if ts >= window_start]
        self._buckets[key] = bucket
        if len(bucket) >= limit.max_per_minute:
            return False
        bucket.append(now)
        return True
