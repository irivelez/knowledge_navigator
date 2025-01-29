import sqlite3
import pandas as pd
from tabulate import tabulate
from bs4 import BeautifulSoup
import os

def clean_text(text):
    """Clean text for display"""
    return BeautifulSoup(text, 'html.parser').get_text().strip()

def evaluate_summaries():
    """Compare original content with summaries"""
    # Get the correct path to knowledge.db
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'knowledge.db')
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"\n❌ Database not found at: {db_path}")
        print("Please run 'python run.py' first to fetch and process articles.")
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Check if table exists
            table_check = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='articles'
            """).fetchone()
            
            if not table_check:
                print("\n❌ Articles table not found!")
                print("Please run 'python run.py' first to create and populate the database.")
                return
            
            # Removed LIMIT 5 to show all articles
            df = pd.read_sql_query("""
                SELECT 
                    title,
                    content,
                    summary,
                    url,
                    source,
                    processed_date
                FROM articles 
                ORDER BY processed_date DESC
            """, conn)
            
            if df.empty:
                print("\n⚠️ No articles found in database.")
                print("Please run 'python run.py' to fetch and process articles.")
                return
            
            print("\n=== Summary Evaluation ===\n")
            print(f"Total articles: {len(df)}\n")
            
            for idx, row in df.iterrows():
                print(f"\n[Article {idx + 1} of {len(df)}]")
                print(f"📰 Title: {row['title']}")
                print(f"📌 Source: {row['source']}")
                print(f"🔗 URL: {row['url']}")
                
                print("\n📝 Original Content:")
                print("-" * 80)
                print(BeautifulSoup(row['content'], 'html.parser').get_text()[:300] + "...")
                
                print("\n📋 Generated Summary:")
                print("-" * 80)
                print(row['summary'])
                print("\n" + "=" * 80)
                
                # Interactive evaluation
                quality = input("\nRate summary quality (1-5, or 'q' to quit): ")
                if quality.lower() == 'q':
                    break
                
                print("\nNext article? (Press Enter to continue, 'q' to quit)")
                if input().lower() == 'q':
                    break
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure the database is properly initialized.")

if __name__ == "__main__":
    evaluate_summaries() 