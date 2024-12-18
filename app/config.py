# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    
    # Topics of Interest
    TOPICS = [
        'AI',
        'Machine Learning',
        'Economics',
        'Entrepreneurship',
        'Technology',
        'Technology Adoption'
    ]
    
    # RSS Feeds by topic
    RSS_FEEDS = {
        'AI & ML': [
            'https://techcrunch.com/feed/',
#           'https://www.technologyreview.com/feed/',
        ],
#        'Economics & Business': [
#            'https://www.economist.com/finance-and-economics/rss.xml',
#            'https://hbr.org/feed'
#        ],
#        'Technology': [
#            'https://www.wired.com/feed/rss',
#            'https://feeds.arstechnica.com/arstechnica/index/'
#        ]
    }
    
    # Learning Settings
    SUMMARY_MAX_LENGTH = 500
    INSIGHTS_MAX_LENGTH = 1000
    BATCH_SIZE = 5