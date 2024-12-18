# tests/test_processor.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime
import time
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import init_db, Content, Base
from app.core.processor import ContentProcessor
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestContentProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        cls.processor = ContentProcessor(test_mode=True)
        
        # Test article for reuse
        cls.test_article = Content(
            title="Google Releases New AI Model",
            content="""
            Google has announced the release of a new AI model called Gemini, 
            which represents a significant advancement in artificial intelligence technology. 
            The model demonstrates superior performance across a wide range of tasks.
            """.strip(),
            source="test",
            url="http://test.com/1",
            published_date=datetime.now()
        )

    def test_rate_limiting(self):
        """Test rate limiting mechanism"""
        print("\nTesting rate limiting...")
        
        test_prompt = "Test prompt"
        requests_made = 0
        
        try:
            # Make several requests quickly
            for i in range(3):
                result = self.processor.generate_text(test_prompt, use_pro=False)
                self.assertTrue(result)
                requests_made += 1
                print(f"✓ Request {requests_made} completed")
            
        except Exception as e:
            self.fail(f"Rate limiting test failed: {str(e)}")

    def test_categorization(self):
        """Test content categorization"""
        print("\nTesting content categorization...")
        
        try:
            category = self.processor.categorize_content(
                self.test_article.title,
                self.test_article.content
            )
            
            print(f"Generated category: {category}")
            self.assertTrue(category)
            self.assertIn(category, Config.CATEGORIES)
            
        except Exception as e:
            self.fail(f"Categorization test failed: {str(e)}")

    def test_summarization(self):
        """Test content summarization"""
        print("\nTesting summarization...")
        
        try:
            summary = self.processor.generate_summary(self.test_article.content)
            print(f"Generated summary: {summary}")
            
            self.assertTrue(summary)
            self.assertIsInstance(summary, str)
            self.assertLess(len(summary), len(self.test_article.content))
            print("✓ Summary generated successfully")
            
        except Exception as e:
            self.fail(f"Summarization test failed: {str(e)}")

    def test_batch_processing(self):
        """Test batch processing functionality"""
        print("\nTesting batch processing...")
        
        # Create test articles
        test_articles = [
            Content(
                title=f"Test Article {i}",
                content=f"Test content for article {i}",
                source="test",
                url=f"http://test.com/{i}",
                published_date=datetime.now()
            )
            for i in range(2)
        ]
        
        try:
            processed, failed = self.processor.process_batch(test_articles, batch_size=1)
            
            print(f"Processed {len(processed)} articles, {len(failed)} failed")
            
            self.assertEqual(len(processed), 2)
            self.assertEqual(len(failed), 0)
            
            for article in processed:
                self.assertTrue(article.category)
                self.assertTrue(article.summary)
                print(f"✓ Article processed: {article.title}")
            
        except Exception as e:
            self.fail(f"Batch processing test failed: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.session.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)