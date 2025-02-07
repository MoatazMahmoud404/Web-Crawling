# Amazon Product Scraper

A high-performance, feature-rich web scraper for Amazon products built with Python and asyncio.

## Features

- 🚀 Asynchronous scraping with rate limiting
- 💾 Multiple output formats (JSON, CSV, SQLite, Markdown)
- 🔄 Proxy and User-Agent rotation
- 🛡️ CAPTCHA detection
- 📊 Detailed metrics and logging
- 🖼️ Media and link extraction
- 📦 File download capabilities
- 🎯 Configurable performance settings
- 📈 Real-time dashboard
- 📝 Markdown output support
- 🛑 External link filtering
- 🔒 Social media link filtering
- 🖼️ External image filtering
- 🗄️ Data compression option

## Requirements

- Python 3.7+
- Required packages (see `requirements.txt`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Moataz404Mahmoud/Web-Crawling.git
cd Web-Crawling
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python main.py
```

## Configuration

The scraper is highly configurable through the `ScraperConfig` class. Key settings include:

### Feature Flags
- `enable_logging`: Enable detailed logging
- `enable_json_output`: Save results as JSON
- `enable_csv_output`: Save results as CSV
- `enable_db_storage`: Store results in SQLite database
- `enable_markdown_output`: 
- `enable_markdown_output`: Save results as Markdown
- `enable_proxy_rotation`: Rotate through proxy servers
- `enable_user_agent_rotation`: Rotate user agents
- `enable_captcha_detection`: Detect and handle CAPTCHAs
- `enable_file_downloads`: Download associated files
- `exclude_external_links`: Filter out external links
- `exclude_social_media_links`: Filter social media links
- `exclude_external_images`: Filter external images
- `compression_enabled`: Enable data compression
- `real_time_dashboard`: Enable real-time monitoring

### Performance Settings
- `max_retries`: Maximum retry attempts
- `retry_delay`: Delay between retries
- `requests_per_second`: Rate limiting
- `max_concurrent_requests`: Concurrency control
- `cache_ttl`: Cache time-to-live
- `chunk_size`: Batch processing size
- `timeout`: Request timeout in seconds
- `max_redirects`: Maximum number of redirects to follow

## Project Structure

```
amazon-scraper/
├── src/
│   ├── __init__.py
│   ├── config.py      # Configuration settings
│   ├── models.py      # Data models
│   ├── utils.py       # Utility functions
│   ├── database.py    # Database operations
│   └── scraper.py     # Main scraper logic
├── main.py            # Entry point
└── README.md
```

## Output

The scraper creates a timestamped output directory containing:
- `amazon_products.json`: Product data in JSON format
- `amazon_products.csv`: Product data in CSV format
- `amazon_products.db`: SQLite database
- `amazon_products.md`: Product data in Markdown format
- `scraper.log`: Detailed logs
- `extracted_links.json`: Extracted links
- `extracted_media.json`: Media information
- `metrics.json`: Performance metrics
- `dashboard.html`: Real-time monitoring dashboard


## Simple Output:

```yaml
================================================================================
                              SCRAPER DASHBOARD
================================================================================

📊 ACTIVE FEATURES:
--------------------------------------------------------------------------------
✅ Detailed Logging               Enabled
✅ JSON Export                    Enabled
✅ CSV Export                     Enabled
✅ Database Storage               Enabled
✅ Proxy Rotation                 Enabled
✅ User-Agent Rotation            Enabled
✅ CAPTCHA Detection              Enabled
✅ File Downloads                 Enabled
✅ External Links Filter          Enabled
✅ Social Media Filter            Enabled
✅ External Images Filter         Enabled
✅ Wait for Images                Enabled
❌ Data Compression               Disabled

⚙️ PERFORMANCE SETTINGS:
--------------------------------------------------------------------------------
🔄 Max Retries: 3
⏱️  Retry Delay: 5 seconds
🚦 Requests Per Second: 2
🔀 Max Concurrent Requests: 5
💾 Cache TTL: 3600 seconds
📦 Processing Chunk Size: 1000 items

🎯 TARGET CONFIGURATION:
--------------------------------------------------------------------------------
📂 Downloads Path: ./amazon_scrape_2025-02-07_12-47/downloads
⏳ Download Wait Time: 10 seconds

🚫 Excluded Domains:
  • facebook.com
  • twitter.com
  • instagram.com

================================================================================

================================================================================
                              SCRAPER STATUS
================================================================================

📈 INITIALIZATION STATUS:
--------------------------------------------------------------------------------
🕒 Start Time: 2025-02-07 12:47:34
📁 Output Directory: amazon_scrape_2025-02-07_12-47
🔍 Keywords to Scrape: 7
🌐 Available Proxies: 3
👤 User Agents: 3

💾 OUTPUT FILES:
--------------------------------------------------------------------------------
📊 JSON Output: amazon_scrape_2025-02-07_12-47\amazon_products.json
📑 CSV Output: amazon_scrape_2025-02-07_12-47\amazon_products.csv
🗄️  Database: amazon_scrape_2025-02-07_12-47\amazon_products.db
📝 Log File: amazon_scrape_2025-02-07_12-47\scraper.log
🔗 Links File: amazon_scrape_2025-02-07_12-47\extracted_links.json
🖼️  Media File: amazon_scrape_2025-02-07_12-47\extracted_media.json
📊 Metrics File: amazon_scrape_2025-02-07_12-47\metrics.json

🎯 TARGET KEYWORDS:
--------------------------------------------------------------------------------
  • Samsung
  • Apple
  • Honor
  • Huawei
  • OnePlus
  • Xiaomi
  • Google Pixel

================================================================================


🚀 Starting scraping process...

[INIT].... → Crawl4AI 0.4.248
[FETCH]... ↓ https://www.amazon.com/s?k=Samsung... | Status: True | Time: 0.14s
[COMPLETE] ● https://www.amazon.com/s?k=Samsung... | Status: True | Total: 0.14s
URL: https://www.amazon.com/s?k=Samsung
Internal links found: 424
External links found: 23
Images found: 248
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=Apple... | Status: True | Time: 0.08s
[COMPLETE] ● https://www.amazon.com/s?k=Apple... | Status: True | Total: 0.08s
URL: https://www.amazon.com/s?k=Apple
Internal links found: 177
External links found: 21
Images found: 75
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=Huawei... | Status: True | Time: 0.14s
[COMPLETE] ● https://www.amazon.com/s?k=Huawei... | Status: True | Total: 0.14s
URL: https://www.amazon.com/s?k=Huawei
Internal links found: 219
External links found: 21
Images found: 100
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=Google+Pixel... | Status: True | Time: 0.15s
[COMPLETE] ● https://www.amazon.com/s?k=Google+Pixel... | Status: True | Total: 0.15s
URL: https://www.amazon.com/s?k=Google+Pixel
Internal links found: 278
External links found: 21
Images found: 95
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=Xiaomi... | Status: True | Time: 0.19s
[COMPLETE] ● https://www.amazon.com/s?k=Xiaomi... | Status: True | Total: 0.19s
URL: https://www.amazon.com/s?k=Xiaomi
Internal links found: 212
External links found: 21
Images found: 90
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=Honor... | Status: True | Time: 0.22s
[COMPLETE] ● https://www.amazon.com/s?k=Honor... | Status: True | Total: 0.22s
URL: https://www.amazon.com/s?k=Honor
Internal links found: 205
External links found: 21
Images found: 94
Videos found: 0
Audio files found: 0
[FETCH]... ↓ https://www.amazon.com/s?k=OnePlus... | Status: True | Time: 0.16s
[COMPLETE] ● https://www.amazon.com/s?k=OnePlus... | Status: True | Total: 0.17s
URL: https://www.amazon.com/s?k=OnePlus
Internal links found: 241
External links found: 21
Images found: 90
Videos found: 0
Audio files found: 0

================================================================================
                              SCRAPING SUMMARY
================================================================================

📊 PERFORMANCE METRICS:
--------------------------------------------------------------------------------
📡 Total Requests: 7
✅ Successful Requests: 7
❌ Failed Requests: 0
📦 Total Products: 131
⬇️  Total Downloads: 0
💾 Total Data Downloaded: 0.00 KB
🚫 CAPTCHAs Encountered: 0
📈 Success Rate: 100.00%
⏱️  Total Time: 8.91 seconds

📂 Data saved in: amazon_scrape_2025-02-07_12-47

================================================================================
```