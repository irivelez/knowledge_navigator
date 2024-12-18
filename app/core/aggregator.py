# app/core/aggregator.py
import feedparser
import logging
from datetime import datetime
import sqlite3
from ..config import Config

logger = logging.getLogger(__name__)

class ContentAggregator:
    def __init__(self, database):
        self.db = database
        self.logger = logging.getLogger(__name__)

    def fetch_articles(self):
        """Fetch articles from configured RSS feeds"""
        articles = []
        
        for topic, feeds in Config.RSS_FEEDS.items():
            for feed_url in feeds:
                try:
                    self.logger.info(f"Fetching from {feed_url}")
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries:
                        # Only process if article doesn't exist
                        if not self._article_exists(entry.get('link', '')):
                            article = {
                                'title': entry.get('title', '').strip(),
                                'content': entry.get('summary', '').strip(),
                                'url': entry.get('link', ''),
                                'source': feed_url,
                                'topic': topic,
                                'published_date': self._parse_date(entry.get('published', ''))
                            }
                            articles.append(article)
                            
                except Exception as e:
                    self.logger.error(f"Error fetching from {feed_url}: {str(e)}")
                    continue
                    
        self.logger.info(f"Fetched {len(articles)} new articles")
        return articles

    def _article_exists(self, url):
        """Check if article already exists in database"""
        with sqlite3.connect(self.db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM articles WHERE url = ?', (url,))
            return cursor.fetchone() is not None

    def _parse_date(self, date_str):
        """Parse date from feed or return current date"""
        if not date_str:
            return datetime.now()
        try:
            return datetime(*feedparser._parse_date(date_str)[:6])
        except:
            return datetime.now()