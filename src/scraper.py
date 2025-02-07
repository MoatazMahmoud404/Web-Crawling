import sqlite3
from concurrent.futures import ThreadPoolExecutor
import asyncio
import json
import logging
import random
import os
import datetime
import time
import pandas as pd
from typing import List, Dict
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from src.config import ScraperConfig
from .models import ScraperMetrics, Cache
from .utils import RateLimiter, Dashboard
from .database import Database


class AmazonScraper:
    def __init__(self, config: ScraperConfig):
        self.config = config
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        self.output_folder = f"Results/amazon_scrape_{self.timestamp}"
        self.setup_directories()
        self.setup_files()
        self.setup_logging()
        self.setup_metrics()

        self.cache = Cache(ttl=self.config.cache_ttl)
        self.rate_limiter = RateLimiter(
            requests_per_second=self.config.requests_per_second)
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)

        self.keywords = ["Samsung", "Apple", "Honor",
                         "Huawei", "OnePlus", "Xiaomi", "Google Pixel"]
        self.base_url = "https://www.amazon.com/s?k="
        self.search_urls = [
            f"{self.base_url}{keyword.replace(' ', '+')}" for keyword in self.keywords]
        self.setup_proxies_and_agents()
        self.setup_configs()

    def setup_directories(self):
        """Set up necessary directories"""
        os.makedirs(self.output_folder, exist_ok=True)
        os.makedirs(self.config.downloads_path, exist_ok=True)

    def setup_files(self):
        """Initialize file paths"""
        self.json_filename = os.path.join(
            self.output_folder, "amazon_products.json")
        self.csv_filename = os.path.join(
            self.output_folder, "amazon_products.csv")
        self.db_filename = os.path.join(
            self.output_folder, "amazon_products.db")
        self.md_filename = os.path.join(
            self.output_folder, "amazon_products.md")
        self.log_filename = os.path.join(self.output_folder, "scraper.log")
        self.links_filename = os.path.join(
            self.output_folder, "extracted_links.json")
        self.media_filename = os.path.join(
            self.output_folder, "extracted_media.json")
        self.metrics_filename = os.path.join(
            self.output_folder, "metrics.json")

    def setup_logging(self):
        """Configure logging"""
        if self.config.enable_logging:
            logging.basicConfig(
                level=logging.INFO,
                filename=self.log_filename,
                filemode="w",
                format="%(asctime)s - %(levelname)s - %(message)s"
            )
            # Add console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            logging.getLogger().addHandler(console_handler)

    def setup_metrics(self):
        """Initialize metrics tracking"""
        self.metrics = ScraperMetrics(start_time=time.time())

    def setup_proxies_and_agents(self):
        """Set up proxy and user agent lists"""
        self.proxies = ["http://proxy1.com:8080",
                        "http://proxy2.com:8080", "http://proxy3.com:8080"]
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        ]

    def setup_configs(self):
        """Set up browser and crawler configurations"""
        self.browser_config = BrowserConfig(
            browser_type="chromium",
            headless=True,
            proxy=random.choice(
                self.proxies) if self.config.enable_proxy_rotation else None,
            user_agent=random.choice(
                self.user_agents) if self.config.enable_user_agent_rotation else None,
            verbose=True,
            accept_downloads=self.config.enable_file_downloads,
            downloads_path=self.config.downloads_path
        )

        self.crawler_config = CrawlerRunConfig(
            extraction_strategy=JsonCssExtractionStrategy(
                schema={
                    "name": "Amazon Product Search Results",
                    "baseSelector": "[data-component-type='s-search-result']",
                    "fields": [
                        {"name": "asin", "selector": "",
                            "type": "attribute", "attribute": "data-asin"},
                        {"name": "title", "selector": "h2 a span", "type": "text"},
                        {"name": "url", "selector": "h2 a",
                            "type": "attribute", "attribute": "href"},
                        {"name": "image", "selector": ".s-image",
                            "type": "attribute", "attribute": "src"},
                        {"name": "rating",
                            "selector": ".a-icon-star-small .a-icon-alt", "type": "text"},
                        {"name": "reviews_count",
                            "selector": "[data-csa-c-func-deps='aui-da-a-popover'] ~ span span", "type": "text"},
                        {"name": "price", "selector": ".a-price .a-offscreen",
                            "type": "text"},
                        {"name": "original_price",
                            "selector": ".a-price.a-text-price .a-offscreen", "type": "text"},
                        {"name": "sponsored",
                            "selector": ".puis-sponsored-label-text", "type": "exists"},
                        {"name": "delivery_info",
                            "selector": "[data-cy='delivery-recipe'] .a-color-base", "type": "text", "multiple": True},
                        {"name": "next_page", "selector": ".s-pagination-next",
                            "type": "attribute", "attribute": "href"},
                        {"name": "captcha_detected",
                            "selector": "#captchacharacters", "type": "exists"},
                    ],
                }
            ),
            cache_mode=CacheMode.ENABLED,
            exclude_external_links=self.config.exclude_external_links,
            exclude_social_media_links=self.config.exclude_social_media_links,
            exclude_external_images=self.config.exclude_external_images,
            wait_for_images=self.config.wait_for_images,
            exclude_domains=self.config.excluded_domains,
            wait_for=self.config.wait_for_downloads
        )

    def print_startup_info(self):
        """Print startup information"""
        print("\n" + "="*80)
        print(" "*30 + "SCRAPER STATUS" + " "*31)
        print("="*80)

        print("\n📈 INITIALIZATION STATUS:")
        print("-"*80)
        print(
            f"🕒 Start Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Output Directory: {self.output_folder}")
        print(f"🔍 Keywords to Scrape: {len(self.keywords)}")
        print(f"🌐 Available Proxies: {len(self.proxies)}")
        print(f"👤 User Agents: {len(self.user_agents)}")

        print("\n💾 OUTPUT FILES:")
        print("-"*80)
        print(f"📊 JSON Output: {self.json_filename}")
        print(f"📑 CSV Output: {self.csv_filename}")
        print(f"🗄️  Database: {self.db_filename}")
        print(f"📝 Log File: {self.log_filename}")
        print(f"🔗 Links File: {self.links_filename}")
        print(f"🖼️  Media File: {self.media_filename}")
        print(f"📊 Metrics File: {self.metrics_filename}")

        print("\n🎯 TARGET KEYWORDS:")
        print("-"*80)
        for keyword in self.keywords:
            print(f"  • {keyword}")

        print("\n" + "="*80 + "\n")

    async def process_url_with_retry(self, url: str, crawler: AsyncWebCrawler) -> Dict:
        """Process a URL with retry logic"""
        for attempt in range(self.config.max_retries):
            try:
                self.metrics.total_requests += 1
                await self.rate_limiter.wait()

                # Check cache first
                cached_data = self.cache.get(url)
                if cached_data:
                    self.metrics.successful_requests += 1
                    return cached_data

                async with self.semaphore:
                    result = await crawler.arun(url=url, config=self.crawler_config)

                if not result.success:
                    raise Exception(result.error_message)

                products = json.loads(result.extracted_content)

                # Handle CAPTCHA detection
                if self.config.enable_captcha_detection and any(p.get("captcha_detected") for p in products):
                    self.metrics.captchas_encountered += 1
                    logging.warning(
                        f"CAPTCHA detected on {url}, changing proxy and retrying...")
                    self.browser_config.proxy = random.choice(self.proxies)
                    continue

                # Save links and media information
                self.save_links_and_media(result, url)

                # Handle downloads
                if self.config.enable_file_downloads:
                    await self.process_downloads(result)

                self.metrics.successful_requests += 1
                self.metrics.total_products += len(products)

                # Cache the results
                self.cache.set(url, products)

                return products

            except Exception as e:
                logging.error(
                    f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                self.metrics.failed_requests += 1
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay)
                else:
                    raise

    async def process_downloads(self, result):
        """Process downloaded files"""
        downloaded_files = result.downloaded_files
        for file in downloaded_files:
            file_size = os.path.getsize(file)
            self.metrics.total_downloads += 1
            self.metrics.total_bytes_downloaded += file_size
            logging.info(f"Downloaded file: {file}, Size: {file_size} bytes")

    def save_links_and_media(self, result, url):
        """Save extracted links and media information"""
        links_data = {
            "url": url,
            "timestamp": datetime.datetime.now().isoformat(),
            "internal_links": result.links.get("internal", []),
            "external_links": result.links.get("external", [])
        }

        media_data = {
            "url": url,
            "timestamp": datetime.datetime.now().isoformat(),
            "images": result.media.get("images", []),
            "videos": result.media.get("videos", []),
            "audio": result.media.get("audio", [])
        }

        self.save_data_compressed(self.links_filename, links_data)
        self.save_data_compressed(self.media_filename, media_data)
        self.log_extraction_stats(links_data, media_data)

    def save_data_compressed(self, filename: str, data: Dict):
        """Save data with optional compression"""
        if self.config.compression_enabled:
            import gzip
            with gzip.open(f"{filename}.gz", 'at') as f:
                f.write(json.dumps(data) + "\n")
        else:
            with open(filename, 'a') as f:
                f.write(json.dumps(data) + "\n")

    def log_extraction_stats(self, links_data: Dict, media_data: Dict):
        """Log extraction statistics"""
        if self.config.enable_logging:
            logging.info(f"URL: {links_data['url']}")
            logging.info(
                f"Internal links found: {len(links_data['internal_links'])}")
            logging.info(
                f"External links found: {len(links_data['external_links'])}")
            logging.info(f"Images found: {len(media_data['images'])}")
            logging.info(f"Videos found: {len(media_data['videos'])}")
            logging.info(f"Audio files found: {len(media_data['audio'])}")

    async def scrape_amazon(self):
        """Main scraping method"""
        # Print configuration dashboard and startup info
        self.config.print_dashboard()
        self.print_startup_info()

        print("\n🚀 Starting scraping process...\n")

        extracted_data = []
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            tasks = []
            for url in self.search_urls:
                tasks.append(self.process_url_with_retry(url, crawler))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logging.error(f"Failed to process URL: {str(result)}")
                else:
                    extracted_data.extend(result)

        await self.save_results(extracted_data)
        self.save_metrics()
        self.print_summary()

    async def save_results(self, extracted_data: List[Dict]):
        """Save results to various outputs"""
        if self.config.enable_json_output:
            self.save_data_compressed(self.json_filename, extracted_data)

        if self.config.enable_csv_output:
            df = pd.DataFrame(extracted_data)
            if self.config.compression_enabled:
                df.to_csv(f"{self.csv_filename}.gz",
                          index=False, compression='gzip')
            else:
                df.to_csv(self.csv_filename, index=False)

        filtered_data = self.filter_data(
            extracted_data, min_rating=4.0, exclude_sponsored=True)

        if self.config.enable_markdown_output:
            self.save_to_markdown(filtered_data)

        if self.config.enable_db_storage:
            await self.save_to_db(extracted_data)

    def filter_data(self, data, min_rating=4.0, exclude_sponsored=True):
        filtered = []
        for product in data:
            try:
                rating = float(product.get("rating", "0").split()[0])
                if rating >= min_rating and (not exclude_sponsored or not product.get("sponsored")):
                    filtered.append(product)
            except ValueError:
                continue
        return filtered

    async def save_to_db(self, data: List[Dict]):
        """Save data to database asynchronously"""
        def db_operation():
            conn = sqlite3.connect(self.db_filename)
            cursor = conn.cursor()

            # Create tables
            self.create_tables(cursor)

            # Process data in chunks
            for i in range(0, len(data), self.config.chunk_size):
                chunk = data[i:i + self.config.chunk_size]
                self.insert_chunk(cursor, chunk)
                conn.commit()

            conn.close()

        with ThreadPoolExecutor() as pool:
            await asyncio.get_event_loop().run_in_executor(pool, db_operation)

    def save_to_markdown(self, data):
        with open(self.md_filename, "w", encoding="utf-8") as f:
            f.write("# Amazon Scraped Products\n\n")
            for product in data:
                f.write(f"## {product.get('title', 'N/A')}\n")
                f.write(f"- **ASIN:** {product.get('asin', 'N/A')}\n")
                f.write(
                    f"- **URL:** [Link](https://www.amazon.com{product.get('url', '')})\n")
                f.write(f"- **Price:** {product.get('price', 'N/A')}\n")
                f.write(f"- **Rating:** {product.get('rating', 'N/A')}\n")
                f.write(f"![Product Image]({product.get('image', '')})\n\n")

    def create_tables(self, cursor):
        """Create database tables"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                asin TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                image TEXT,
                rating TEXT,
                reviews_count TEXT,
                price TEXT,
                original_price TEXT,
                sponsored TEXT,
                delivery_info TEXT
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                href TEXT,
                text TEXT,
                title TEXT,
                base_domain TEXT,
                link_type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                src TEXT,
                alt TEXT,
                type TEXT,
                score INTEGER,
                width INTEGER,
                height INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")

        # Add indexes for better query performance
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_products_asin ON products(asin)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_links_url ON links(url)")
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_media_url ON media(url)")

    def insert_chunk(self, cursor, chunk: List[Dict]):
        """Insert a chunk of data into the database"""
        for product in chunk:
            cursor.execute(
                "INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    product.get("asin"), product.get(
                        "title"), product.get("url"),
                    product.get("image"), product.get(
                        "rating"), product.get("reviews_count"),
                    product.get("price"), product.get("original_price"),
                    str(product.get("sponsored")), str(
                        product.get("delivery_info"))
                )
            )

    def save_metrics(self):
        """Save metrics to file"""
        metrics_data = {
            "total_requests": self.metrics.total_requests,
            "successful_requests": self.metrics.successful_requests,
            "failed_requests": self.metrics.failed_requests,
            "total_products": self.metrics.total_products,
            "total_downloads": self.metrics.total_downloads,
            "total_bytes_downloaded": self.metrics.total_bytes_downloaded,
            "captchas_encountered": self.metrics.captchas_encountered,
            "success_rate": self.metrics.get_success_rate(),
            "elapsed_time": self.metrics.get_elapsed_time()
        }

        with open(self.metrics_filename, 'w') as f:
            json.dump(metrics_data, f, indent=4)

    def print_summary(self):
        """Print scraping summary"""
        print("\n" + "="*80)
        print(" "*30 + "SCRAPING SUMMARY" + " "*30)
        print("="*80)

        print("\n📊 PERFORMANCE METRICS:")
        print("-"*80)
        print(f"📡 Total Requests: {self.metrics.total_requests}")
        print(f"✅ Successful Requests: {self.metrics.successful_requests}")
        print(f"❌ Failed Requests: {self.metrics.failed_requests}")
        print(f"📦 Total Products: {self.metrics.total_products}")
        print(f"⬇️  Total Downloads: {self.metrics.total_downloads}")
        print(
            f"💾 Total Data Downloaded: {self.metrics.total_bytes_downloaded / 1024:.2f} KB")
        print(f"🚫 CAPTCHAs Encountered: {self.metrics.captchas_encountered}")
        print(f"📈 Success Rate: {self.metrics.get_success_rate():.2f}%")
        print(f"⏱️  Total Time: {self.metrics.get_elapsed_time():.2f} seconds")

        print(f"\n📂 Data saved in: {self.output_folder}")
        print("\n" + "="*80)
