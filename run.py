# run.py
import logging
from app.core.aggregator import ContentAggregator
from app.core.processor import ContentProcessor
from app.database.models import Database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize components
        aggregator = ContentAggregator()
        processor = ContentProcessor()
        db = Database()
        
        # Fetch and process articles
        articles = aggregator.fetch_articles()
        logger.info(f"Fetched {len(articles)} new articles")
        
        if not articles:
            logger.info("No new articles to process")
            return
        
        # Process articles
        processed_articles = []
        for article in articles:
            processed_article, error = processor.process_article(article)
            if error:
                logger.error(f"Error processing article: {error}")
                continue
            processed_articles.append(processed_article)
        
        # Group articles and save
        grouped_articles = processor.group_articles_by_topic(processed_articles)
        for topic, group_data in grouped_articles.items():
            if group_data and group_data['articles']:
                for article_dict in group_data['articles']:
                    article_dict['topic_group'] = topic
                    db.save_processed_article(article_dict)
        
        logger.info("Processing completed")
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        logger.info("Processing completed")
        raise e

if __name__ == "__main__":
    main()