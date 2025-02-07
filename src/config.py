from dataclasses import dataclass
from typing import Dict, List
import datetime


@dataclass
class ScraperConfig:
    def __init__(self):
        self.enable_logging: bool = True
        self.enable_json_output: bool = True
        self.enable_csv_output: bool = True
        self.enable_db_storage: bool = True
        self.enable_markdown_output: bool = True  # New feature
        self.enable_proxy_rotation: bool = True
        self.enable_user_agent_rotation: bool = True
        self.enable_captcha_detection: bool = True
        # File download features
        self.enable_file_downloads: bool = True
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.downloads_path: str = f"./Results/amazon_scrape_{self.timestamp}/downloads"
        self.wait_for_downloads: int = 10
        # Link and media features
        self.exclude_external_links: bool = True
        self.exclude_social_media_links: bool = True
        self.exclude_external_images: bool = True
        self.wait_for_images: bool = True
        self.excluded_domains: list = [
            "facebook.com", "twitter.com", "instagram.com"]
        # Optimization features
        self.max_retries: int = 3
        self.retry_delay: int = 5
        self.requests_per_second: int = 2
        self.max_concurrent_requests: int = 5
        self.cache_ttl: int = 3600  # 1 hour
        self.chunk_size: int = 1000  # For batch processing
        self.compression_enabled: bool = False

        # Add some descriptive names for the dashboard
        self.feature_descriptions = {
            "enable_logging": "Detailed Logging",
            "enable_json_output": "JSON Export",
            "enable_csv_output": "CSV Export",
            "enable_db_storage": "Database Storage",
            "enable_proxy_rotation": "Proxy Rotation",
            "enable_user_agent_rotation": "User-Agent Rotation",
            "enable_captcha_detection": "CAPTCHA Detection",
            "enable_file_downloads": "File Downloads",
            "exclude_external_links": "External Links Filter",
            "enable_markdown_output": "Markdown Export",
            "exclude_social_media_links": "Social Media Filter",
            "exclude_external_images": "External Images Filter",
            "wait_for_images": "Wait for Images",
            "compression_enabled": "Data Compression"
        }

    def print_dashboard(self):
        """Print a dashboard of current configuration and settings"""
        print("\n" + "="*80)
        print(" "*30 + "SCRAPER DASHBOARD" + " "*30)
        print("="*80)

        # Active Features Section
        print("\n📊 ACTIVE FEATURES:")
        print("-"*80)
        for key, description in self.feature_descriptions.items():
            status = getattr(self, key)
            status_symbol = "✅" if status else "❌"
            print(
                f"{status_symbol} {description:<30} {'Enabled' if status else 'Disabled'}")

        # Performance Settings Section
        print("\n⚙️ PERFORMANCE SETTINGS:")
        print("-"*80)
        print(f"🔄 Max Retries: {self.max_retries}")
        print(f"⏱️  Retry Delay: {self.retry_delay} seconds")
        print(f"🚦 Requests Per Second: {self.requests_per_second}")
        print(f"🔀 Max Concurrent Requests: {self.max_concurrent_requests}")
        print(f"💾 Cache TTL: {self.cache_ttl} seconds")
        print(f"📦 Processing Chunk Size: {self.chunk_size} items")

        # Target Configuration Section
        print("\n🎯 TARGET CONFIGURATION:")
        print("-"*80)
        print(f"📂 Downloads Path: {self.downloads_path}")
        print(f"⏳ Download Wait Time: {self.wait_for_downloads} seconds")
        print("\n🚫 Excluded Domains:")
        for domain in self.excluded_domains:
            print(f"  • {domain}")

        print("\n" + "="*80)
