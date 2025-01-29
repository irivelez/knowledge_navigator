# app/core/aggregator.py
import feedparser
import logging
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)

class ContentAggregator:
    def __init__(self):
        self.feeds = [
            'https://techcrunch.com/feed/',
            'https://feeds.arstechnica.com/arstechnica/index/',
            'https://www.technologyreview.com/feed/',
            'https://www.artificialintelligence-news.com/feed/'
        ]
        self.articles_per_feed = 3  # Keep 3 articles per source
        
    def fetch_articles(self):
        """Fetch latest articles from configured feeds"""
        articles = []
        
        for feed_url in self.feeds:
            try:
                logger.info(f"Fetching from {feed_url}")
                feed = feedparser.parse(feed_url)
                
                # Get latest N articles from each feed
                for entry in feed.entries[:self.articles_per_feed]:
                    article = {
                        'title': entry.get('title', '').strip(),
                        'content': entry.get('summary', '').strip(),
                        'url': entry.get('link', ''),
                        'source': feed_url,
                        'published_date': entry.get('published', '')
                    }
                    articles.append(article)
                    
            except Exception as e:
                logger.error(f"Error fetching from {feed_url}: {str(e)}")
                continue
                
        logger.info(f"Fetched {len(articles)} articles")
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