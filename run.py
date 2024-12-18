# run.py
from app.database.models import Database
from app.core.aggregator import ContentAggregator
from app.core.processor import ContentProcessor
from app.core.insights import InsightsManager
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('knowledge_navigator.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        logger.info("Initializing components...")
        db = Database()
        aggregator = ContentAggregator(db)
        processor = ContentProcessor()
        insights = InsightsManager(db)
        
        # Fetch new articles
        logger.info("Fetching new articles...")
        articles = aggregator.fetch_articles()
        logger.info(f"Fetched {len(articles)} new articles")
        
        if not articles:
            logger.info("No new articles to process")
            return
        
        # Process articles
        processed, failed = processor.process_batch(articles)
        
        # Save processed articles
        for article in processed:
            db.save_processed_article(article)
        
        # Log results with concepts
        logger.info("Processing Results:")
        logger.info(f"Successfully processed: {len(processed)} articles")
        logger.info(f"Failed to process: {len(failed)} articles")
        
        # Display sample results
        if processed:
            sample = processed[0]
            logger.info("\nSample Processed Article:")
            logger.info(f"Title: {sample.get('title', 'Unknown')}")
            logger.info(f"Summary: {sample.get('summary', 'No summary generated')}")
            logger.info(f"Key Concepts: {sample.get('key_concepts', 'No concepts extracted')}")
        
        if failed:
            logger.warning("\nSample Failed Articles:")
            for article, error in failed[:3]:  # Show first 3 failures
                logger.warning(f"Article: {article.get('title', 'Unknown')}")
                logger.warning(f"Error: {error}")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Processing completed")

if __name__ == "__main__":
    main()