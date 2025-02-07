import asyncio
import time


class RateLimiter:
    """Rate limiter for controlling request frequency"""

    def __init__(self, requests_per_second: int = 2):
        self.requests_per_second = requests_per_second
        self.minimum_interval = 1.0 / requests_per_second
        self.last_request_time = 0

    async def wait(self):
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.minimum_interval:
            await asyncio.sleep(self.minimum_interval - elapsed)
        self.last_request_time = time.time()


class Dashboard:
    """Class for handling dashboard display"""
    @staticmethod
    def print_separator():
        print("\n" + "="*80)

    @staticmethod
    def print_header(title: str):
        Dashboard.print_separator()
        print(" "*30 + title + " "*30)
        Dashboard.print_separator()

    @staticmethod
    def print_section(title: str):
        print(f"\n{title}")
        print("-"*80)
