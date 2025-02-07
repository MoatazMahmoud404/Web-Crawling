import asyncio
from src.config import ScraperConfig
from src.scraper import AmazonScraper


async def main():
    """Main entry point for the Amazon scraper"""
    config = ScraperConfig()
    scraper = AmazonScraper(config)
    await scraper.scrape_amazon()

if __name__ == "__main__":
    asyncio.run(main())
