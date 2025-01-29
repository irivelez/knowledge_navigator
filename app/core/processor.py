# app/core/processor.py
from bs4 import BeautifulSoup
from huggingface_hub import InferenceClient
from datetime import datetime
import logging
import time
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class ContentProcessor:
    def __init__(self):
        # Get API token from environment
        self.hf_token = os.getenv('HUGGINGFACE_API_KEY')
        if not self.hf_token:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
            
        # Initialize clients
        self.client = InferenceClient(token=self.hf_token)
        self.summarization_model = "facebook/bart-large-cnn"  # For factual summaries
        self.analysis_model = "gpt2"  # For insights generation (optional)
        self.gemma_url = "https://api-inference.huggingface.co/models/google/gemma-2-2b-it"
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
        logger.info("Initializing ContentProcessor with Hugging Face Inference API")
        
        self.topic_groups = {
            'AI_ML': ['ai', 'machine learning', 'neural', 'gpt', 'llm', 'artificial intelligence', 'chatgpt', 'openai', 'model', 'deep learning'],
            'Business': ['startup', 'funding', 'acquisition', 'partnership', 'launch', 'announces', 'market', 'investment'],
            'Cybersecurity': ['security', 'breach', 'hack', 'privacy', 'vulnerability', 'data', 'cyber', 'protection'],
            'Innovation': ['research', 'breakthrough', 'innovation', 'development', 'discovery', 'patent', 'scientific', 'future'],
            'Tech': []  # Default category
        }

    def process_article(self, article):
        try:
            if not article.get('content'):
                return article, "No content to process"

            # Clean HTML tags and normalize spaces
            clean_content = BeautifulSoup(article['content'], 'html.parser').get_text()
            clean_content = ' '.join(clean_content.split())

            # Get factual summary using BART
            summary_response = self.client.summarization(
                clean_content[:1024],
                model=self.summarization_model,
                clean_up_tokenization_spaces=True,
                truncation="longest_first"
            )
            
            summary = summary_response.get('summary_text', '').strip() if isinstance(summary_response, dict) else str(summary_response).strip()

            # Update article
            article.update({
                'summary': summary,
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

    def get_insights(self, articles, topic):
        """Generate insights using Gemma model"""
        try:
            # Prepare richer context from articles
            context = []
            for article in articles[:8]:  # Take up to 5 articles for context
                context.append(f"Title: {article['title']}")
                context.append(f"Summary: {article.get('summary', 'No summary available')}\n")
            
            context_text = "\n".join(context)
            
            prompt = f"""Based on these {topic} news articles and as a tech analyst, provide 3 key insights about the current state and trends in this field:

{context_text}

Please provide 3 clear insights about these developments in {topic}. Each insight should be a complete statement about the trends or implications shown in these articles."""

            logger.info(f"Generating insights for {topic} with {len(articles)} articles")
            
            response = requests.post(
                self.gemma_url,
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 300,
                        "temperature": 0.5,  # Lower temperature for more focused responses
                        "top_p": 0.95,
                        "return_full_text": False
                    }
                }
            )
            
            logger.info(f"Gemma API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                logger.info(f"Gemma Response: {response_data}")
                
                if isinstance(response_data, list) and response_data:
                    insights_text = response_data[0].get('generated_text', '')
                    # Clean and format insights
                    insights = [
                        insight.strip()
                        for insight in insights_text.split('\n')
                        if insight.strip() and 
                        not insight.lower().startswith('key insight') and
                        not insight.startswith('Please provide') and
                        not insight.startswith('Based on') and
                        len(insight.strip()) > 20  # Ensure meaningful length
                    ]
                    
                    if not insights:  # If no valid insights found
                        return [
                            f"Major developments in {topic} show increasing industry focus",
                            f"Multiple companies are advancing {topic.lower()} capabilities",
                            "Innovation continues to drive industry transformation"
                        ]
                    
                    return insights[:3]
                
            logger.warning(f"Unexpected response format from Gemma API: {response.text}")
            return [
                f"Significant advances in {topic} technology",
                "Industry leaders driving innovation",
                "New applications emerging rapidly"
            ]
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return [
                f"Key trends emerging in {topic}",
                "Industry developments show promising direction",
                "Innovation continues to shape the landscape"
            ]

    def group_articles_by_topic(self, articles):
        """Group articles based on their main topics with insights"""
        groups = {topic: [] for topic in self.topic_groups.keys()}
        
        for article in articles:
            title_lower = article['title'].lower()
            content_lower = article.get('content', '').lower()
            summary_lower = article.get('summary', '').lower()
            
            # Classify based on keywords
            classified = False
            for topic, keywords in self.topic_groups.items():
                if topic != 'Tech' and keywords and any(
                    keyword in title_lower or 
                    keyword in content_lower or 
                    keyword in summary_lower 
                    for keyword in keywords):
                    groups[topic].append(article)
                    classified = True
                    break
            
            if not classified:
                groups['Tech'].append(article)

        # Process insights for each group
        insights = {}
        for topic, topic_articles in groups.items():
            if topic_articles:
                topic_insights = self.get_insights(topic_articles, topic)
                insights[topic] = {
                    'count': len(topic_articles),
                    'sources': list(set(a['source'] for a in topic_articles)),
                    'insights': topic_insights,
                    'articles': topic_articles
                }
            else:
                insights[topic] = None

        return insights

def group_articles_by_topic(articles):
    """Group articles based on their main topics"""
    groups = {
        'AI_ML': [],
        'Business': [],
        'Cybersecurity': [],
        'Innovation': [],
        'Tech': []
    }
    
    # Keywords for classification
    keywords = {
        'AI_ML': ['ai', 'machine learning', 'neural', 'gpt', 'llm', 'artificial intelligence', 'model'],
        'Business': ['startup', 'funding', 'acquisition', 'partnership'],
        'Cybersecurity': ['security', 'breach', 'hack', 'privacy', 'vulnerability'],
        'Innovation': ['research', 'breakthrough', 'innovation', 'development']
    }
    
    for article in articles:
        title_lower = article['title'].lower()
        content_lower = article['content'].lower()
        
        # Classify based on keywords
        classified = False
        for topic, topic_keywords in keywords.items():
            if any(keyword in title_lower or keyword in content_lower for keyword in topic_keywords):
                groups[topic].append(article)
                classified = True
                break
        
        if not classified:
            groups['Tech'].append(article)
    
    return groups