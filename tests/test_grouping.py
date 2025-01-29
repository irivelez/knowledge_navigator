import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import os

def evaluate_grouping():
    """Evaluate article grouping results"""
    # Get the correct path to knowledge.db
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(current_dir), 'knowledge.db')
    
    if not os.path.exists(db_path):
        print(f"\n❌ Database not found at: {db_path}")
        print("Please run 'python run.py' first to fetch and process articles.")
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            # Get articles grouped by topic
            df = pd.read_sql_query("""
                SELECT 
                    topic_group,
                    COUNT(*) as article_count,
                    GROUP_CONCAT(title, ' | ') as titles
                FROM articles 
                GROUP BY topic_group
                ORDER BY topic_group
            """, conn)
            
            print("\n=== Article Grouping Analysis ===\n")
            
            # Show overall statistics
            print(f"Total Groups Found: {len(df)}")
            print("\nDistribution by Topic:")
            print("-" * 40)
            
            # Show each group's content
            for _, row in df.iterrows():
                print(f"\n📑 Topic Group: {row['topic_group']}")
                print(f"📊 Articles in group: {row['article_count']}")
                print("\n📰 Articles:")
                for idx, title in enumerate(row['titles'].split(' | '), 1):
                    print(f"{idx}. {title}")
                print("-" * 40)
            
            # Show detailed view option
            while True:
                group = input("\nEnter topic group to see details (or 'q' to quit): ")
                if group.lower() == 'q':
                    break
                
                articles = pd.read_sql_query("""
                    SELECT 
                        title,
                        summary,
                        source,
                        url
                    FROM articles 
                    WHERE topic_group = ?
                    ORDER BY processed_date DESC
                """, conn, params=[group])
                
                if not articles.empty:
                    print(f"\n=== Articles in {group} ===\n")
                    for _, article in articles.iterrows():
                        print(f"📰 {article['title']}")
                        print(f"📌 Source: {article['source']}")
                        print(f"🔗 URL: {article['url']}")
                        print(f"📝 Summary: {article['summary']}\n")
                        print("-" * 40)
                else:
                    print(f"No articles found in group: {group}")
    
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure the database is properly initialized.")

if __name__ == "__main__":
    evaluate_grouping() 