"""Simple in-memory rate limiter per client IP / key."""
import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import HTTPException, status


class SimpleRateLimiter:
    """Sliding-window rate limiter."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)

    def check(self, client_id: str):
        now = time.time()
        window_start = now - self.window_seconds

        # Clean old timestamps
        timestamps = [t for t in self.requests[client_id] if t > window_start]
        self.requests[client_id] = timestamps

        if len(timestamps) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please wait before asking another question.",
            )

        self.requests[client_id].append(now)


rate_limiter = SimpleRateLimiter(max_requests=60, window_seconds=60)
