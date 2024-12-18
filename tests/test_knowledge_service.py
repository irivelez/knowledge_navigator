# tests/test_knowledge_service.py
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
import logging
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.models import init_db, Content, Base
from app.core.knowledge_service import KnowledgeService
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestKnowledgeService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize test environment"""
        # Use in-memory SQLite for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        
        # Initialize service with test mode enabled
        cls.knowledge_service = KnowledgeService(cls.session, test_mode=True)

    def setUp(self):
        """Clear database before each test"""
        self.session.query(Content).delete()
        self.session.commit()

    def test_complete_workflow_small(self):
        """Test the complete workflow with mock data"""
        print("\nTesting complete workflow with mock data...")
        
        try:
            # Run the complete workflow
            total_articles, processed_count, error_count = self.knowledge_service.update_knowledge_base()
            
            # Get stats
            stats = self.knowledge_service.get_content_stats()
            
            print(f"\nWorkflow results:")
            print(f"Total articles: {stats['total_articles']}")
            print(f"Processed articles: {stats['processed_articles']}")
            print(f"Failed/Error articles: {error_count}")
            
            # Verify results
            self.assertGreater(stats['total_articles'], 0)
            self.assertEqual(error_count, 0)
            
            # Check content
            processed = self.session.query(Content).all()
            for article in processed:
                self.assertIsNotNone(article.category)
                self.assertIsNotNone(article.summary)
                print(f"\nProcessed article:")
                print(f"Title: {article.title}")
                print(f"Category: {article.category}")
                print(f"Summary: {article.summary}")
            
        except Exception as e:
            self.fail(f"Workflow failed: {str(e)}")

    def test_incremental_update(self):
        """Test incremental updates with mock data"""
        print("\nTesting incremental updates...")
        
        # First update
        total_1, processed_1, error_1 = self.knowledge_service.update_knowledge_base()
        initial_count = self.session.query(Content).count()
        print(f"Initial update: {initial_count} articles, {error_1} errors")
        
        # Second update (should not duplicate articles)
        total_2, processed_2, error_2 = self.knowledge_service.update_knowledge_base()
        final_count = self.session.query(Content).count()
        print(f"Second update: {final_count} articles, {error_2} errors")
        
        # Verify no duplicates
        self.assertEqual(final_count, initial_count)
        self.assertEqual(error_1 + error_2, 0)

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.session.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)