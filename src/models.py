from dataclasses import dataclass
import time
from typing import List, Dict, Any
import hashlib

@dataclass
class ScraperMetrics:
    """Class for tracking scraper metrics"""
    start_time: float
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_products: int = 0
    total_downloads: int = 0
    total_bytes_downloaded: int = 0
    captchas_encountered: int = 0

    def get_success_rate(self) -> float:
        return (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0

    def get_elapsed_time(self) -> float:
        return time.time() - self.start_time


class Cache:
    """Cache implementation for storing scraped data"""
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Any] = {}
        self.ttl = ttl

    def _get_key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()

    def get(self, url: str) -> Any:
        key = self._get_key(url)
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp <= self.ttl:
                return data
            del self.cache[key]
        return None

    def set(self, url: str, data: Any):
        key = self._get_key(url)
        self.cache[key] = (data, time.time())