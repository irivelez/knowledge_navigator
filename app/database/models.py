# app/database/models.py
import sqlite3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name='knowledge.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        """Initialize database with updated schema"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    content TEXT,
                    summary TEXT,
                    url TEXT UNIQUE,
                    source TEXT,
                    topic_group TEXT,
                    processed_date TEXT
                )
            ''')
            conn.commit()

    def save_processed_article(self, article):
        """Save processed article to database"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO articles 
                (title, content, summary, url, source, topic_group, processed_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article.get('content', ''),
                article.get('summary', ''),
                article['url'],
                article.get('source', ''),
                article.get('topic_group', ''),
                datetime.now().isoformat()
            ))
            conn.commit()

    def get_todays_articles(self):
        """Get only today's articles"""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            today = datetime.now().date().strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT 
                    title,
                    content,
                    summary,
                    url,
                    source,
                    topic_group,
                    processed_date
                FROM articles 
                WHERE DATE(processed_date) = ?
                ORDER BY processed_date DESC
            ''', (today,))
            
            return [dict(row) for row in cursor.fetchall()]