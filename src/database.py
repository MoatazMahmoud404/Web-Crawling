import sqlite3
from typing import List, Dict
import logging

class Database:
    """Database handler for storing scraped data"""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create products table
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

            # Create links table
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

            # Create media table
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

            # Add indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_asin ON products(asin)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_url ON links(url)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_media_url ON media(url)")

    def insert_products(self, products: List[Dict]):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for product in products:
                    cursor.execute(
                        "INSERT OR IGNORE INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            product.get("asin"), product.get("title"), product.get("url"),
                            product.get("image"), product.get("rating"), product.get("reviews_count"),
                            product.get("price"), product.get("original_price"),
                            str(product.get("sponsored")), str(product.get("delivery_info"))
                        )
                    )
        except Exception as e:
            logging.error(f"Database error: {str(e)}")
            raise