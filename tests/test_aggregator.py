# validate.py
import os
from dotenv import load_dotenv
from content_navigator import ContentNavigator
import logging
from datetime import datetime

# Load environment variables
load_dotenv()

def validate_api_connection(navigator):
    """Test API connection and simple generation"""
    print("\n1. Testing Hugging Face API Connection:")
    try:
        test_prompt = "Summarize this: AI technology is advancing rapidly."
        response = navigator.client.text_generation(test_prompt)
        print("✓ API Connection successful")
        print(f"Sample response: {response.strip()}")
        return True
    except Exception as e:
        print(f"✗ API Connection failed: {str(e)}")
        return False

def validate_rss_feeds(navigator):
    """Test RSS feed fetching"""
    print("\n2. Testing RSS Feeds:")
    try:
        articles = navigator.fetch_content()
        print(f"✓ Found {len(articles)} new articles")
        if articles:
            # Display sample article
            sample = articles[0]
            print("\nSample Article:")
            print(f"Title: {sample['title']}")
            print(f"Source: {sample['source']}")
            print(f"Content preview: {sample['content'][:200]}...")
        return True
    except Exception as e:
        print(f"✗ RSS Fetching failed: {str(e)}")
        return False

def validate_processing(navigator):
    """Test article processing"""
    print("\n3. Testing Article Processing:")
    try:
        # Create test article from real feed
        articles = navigator.fetch_content()
        if not articles:
            print("No articles available for processing test")
            return False
            
        test_article = articles[0]
        processed = navigator.process_article(test_article)
        
        print("✓ Processing successful")
        print("\nProcessing Results:")
        print(f"Title: {processed['title']}")
        print(f"Category: {processed['category']}")
        print(f"Summary: {processed['summary']}")
        print(f"Insights: {processed['insights']}")
        return True
    except Exception as e:
        print(f"✗ Processing failed: {str(e)}")
        return False

def validate_database(navigator):
    """Test database operations"""
    print("\n4. Testing Database Operations:")
    try:
        # Test article storage
        articles = navigator.fetch_content()
        if articles:
            test_article = navigator.process_article(articles[0])
            navigator.store_article(test_article)
            print("✓ Article storage successful")
            
            # Verify storage
            if navigator._article_exists(test_article['url']):
                print("✓ Article retrieval successful")
            else:
                print("✗ Article retrieval failed")
        return True
    except Exception as e:
        print(f"✗ Database operations failed: {str(e)}")
        return False

def validate_full_workflow(navigator):
    """Test complete workflow"""
    print("\n5. Testing Complete Workflow:")
    try:
        navigator.run()
        print("✓ Full workflow completed successfully")
        return True
    except Exception as e:
        print(f"✗ Workflow failed: {str(e)}")
        return False

def main():
    print("Starting Content Navigator Validation")
    print("=====================================")
    
    try:
        navigator = ContentNavigator()
        
        # Run validations
        api_ok = validate_api_connection(navigator)
        rss_ok = validate_rss_feeds(navigator)
        processing_ok = validate_processing(navigator)
        db_ok = validate_database(navigator)
        workflow_ok = validate_full_workflow(navigator)
        
        # Summary
        print("\nValidation Summary:")
        print("==================")
        print(f"API Connection:    {'✓' if api_ok else '✗'}")
        print(f"RSS Feeds:         {'✓' if rss_ok else '✗'}")
        print(f"Article Processing:{'✓' if processing_ok else '✗'}")
        print(f"Database:          {'✓' if db_ok else '✗'}")
        print(f"Full Workflow:     {'✓' if workflow_ok else '✗'}")
        
    except Exception as e:
        print(f"\nValidation failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()