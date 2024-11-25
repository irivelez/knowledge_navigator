import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # API Keys
    NEWS_API_KEY = os.getenv('NEWS_API_KEY')
    
    # Sources
    RSS_FEEDS = os.getenv('RSS_FEEDS', '').split(',')
    WEB_SOURCES = os.getenv('WEB_SOURCES', '').split(',')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./knowledge_navigator.db')
    
    # Content Categories
    CATEGORIES = [
        'AI & Technology',
        'Future Studies',
        'Innovation',
        'Entrepreneurship',
        'Economics',
        'Other'
    ]
    
    # Model Configuration
    MODEL_NAME = "google/gemma-2b"
    MAX_LENGTH = 512
    
    # Update Frequency (in minutes)
    CONTENT_UPDATE_FREQUENCY = 60