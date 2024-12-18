# app/core/processor.py
from huggingface_hub import InferenceClient
from datetime import datetime
import logging
import time
import os
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self):
        self.client = InferenceClient(token=os.getenv('HUGGINGFACE_API_KEY'))
        self.model = "facebook/bart-large-cnn"
        self.timeout = 30
        self.max_retries = 3
        self.retry_delay = 2

    def process_article(self, article):
        try:
            if not article.get('content'):
                return article, "No content to process"

            # Clean HTML tags from content
            clean_content = BeautifulSoup(article['content'], 'html.parser').get_text()
            
            # 1. Get summary first - simple API call
            summary_response = self.client.summarization(
                clean_content[:1024],
                model=self.model
            )
            
            summary = summary_response.get('summary_text', '').strip() if isinstance(summary_response, dict) else str(summary_response).strip()

            # 2. Get concepts - simple API call with clean prompt
            concepts_prompt = (
                "Output only 3-5 main technical terms as comma-separated values: " + summary
            )
            
            concepts_response = self.client.summarization(
                concepts_prompt,
                model=self.model
            )
            
            concepts = concepts_response.get('summary_text', '').strip()

            article.update({
                'summary': summary,
                'key_concepts': concepts,
                'model_used': self.model,
                'processed_date': datetime.now()
            })

            logger.info(f"Successfully processed article: {article.get('title', 'Unknown')}")
            return article, None

        except Exception as e:
            error_msg = f"Error processing article: {str(e)}"
            logger.error(error_msg)
            return article, error_msg

    def process_batch(self, articles):
        processed = []
        failed = []
        
        for article in articles:
            processed_article, error = self.process_article(article)
            if error:
                failed.append((article, error))
            else:
                processed.append(processed_article)
            
            # Small delay between articles
            time.sleep(2)
        
        logger.info(f"Batch processing completed. Processed: {len(processed)}, Failed: {len(failed)}")
        return processed, failed