# app/database/models.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='knowledge.db'):
        self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT UNIQUE,
                    source TEXT,
                    topic TEXT,          -- AI, ML, Economics, etc.
                    key_concepts TEXT,    -- Main concepts identified
                    summary TEXT,         -- Brief summary
                    insights TEXT,        -- Learning insights
                    practical_apps TEXT,  -- Practical applications
                    related_concepts TEXT,-- Related topics/concepts
                    published_date DATETIME,
                    processed_date DATETIME
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS concepts (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    description TEXT,
                    frequency INTEGER,    -- How often it appears
                    last_seen DATETIME
                )
            ''')

    def save_processed_article(self, article):
        """Save article with its concepts"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT INTO articles (
                    title, content, url, source,
                    summary, key_concepts, 
                    processed_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                article['title'],
                article['content'],
                article['url'],
                article['source'],
                article['summary'],
                article['key_concepts'],
                article['processed_date']
            ))
            conn.commit()