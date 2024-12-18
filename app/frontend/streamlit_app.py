import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

def connect_to_db():
    # Get the absolute path to knowledge.db
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'knowledge.db')
    
    if not os.path.exists(db_path):
        st.error(f"Database not found at: {db_path}")
        return None
        
    return sqlite3.connect(db_path)

def main():
    st.set_page_config(
        page_title="Tech Articles Summarizer",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Tech Articles Summarizer")
    st.subheader("TechCrunch Articles - Summaries and Key Concepts")
    
    # Add description
    st.markdown("""
    This tool provides summaries and key concepts from recent TechCrunch articles. 
    Browse the latest tech news in a condensed format.
    """)
    
    # Connect to database
    conn = connect_to_db()
    if conn is None:
        st.error("Could not connect to database. Please ensure knowledge.db exists.")
        return
    
    # Sidebar for filtering
    st.sidebar.title("Filters")
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["Latest Articles", "Concept Explorer", "Search"])
    
    with tab1:
        st.header("Latest Processed Articles")
        
        # Get latest articles
        df = pd.read_sql_query("""
            SELECT 
                title,
                summary,
                key_concepts,
                processed_date,
                url
            FROM articles 
            ORDER BY processed_date DESC 
            LIMIT 10
        """, conn)
        
        # Display each article in a card-like format
        for _, row in df.iterrows():
            with st.expander(row['title']):
                st.write("**Summary:**")
                st.write(row['summary'])
                st.write("**Key Concepts:**")
                st.write(row['key_concepts'])
                st.write(f"**Source:** [{row['url']}]({row['url']})")
                st.write(f"Processed: {row['processed_date']}")
    
    with tab2:
        st.header("Concept Explorer")
        
        # Get unique concepts
        concepts_df = pd.read_sql_query("""
            SELECT DISTINCT key_concepts 
            FROM articles 
            WHERE key_concepts IS NOT NULL
        """, conn)
        
        # Create a list of all concepts
        all_concepts = []
        for concepts in concepts_df['key_concepts']:
            if concepts:
                all_concepts.extend([c.strip() for c in concepts.split(',')])
        unique_concepts = sorted(set(all_concepts))
        
        # Concept selection
        selected_concept = st.selectbox("Select a concept to explore:", unique_concepts)
        
        if selected_concept:
            # Find articles with this concept
            related_articles = pd.read_sql_query("""
                SELECT title, summary, url 
                FROM articles 
                WHERE key_concepts LIKE ?
                ORDER BY processed_date DESC
            """, conn, params=[f'%{selected_concept}%'])
            
            st.write(f"Found {len(related_articles)} articles about {selected_concept}")
            
            for _, article in related_articles.iterrows():
                with st.expander(article['title']):
                    st.write(article['summary'])
                    st.write(f"[Read more]({article['url']})")
    
    with tab3:
        st.header("Search Articles")
        search_term = st.text_input("Enter search term:")
        
        if search_term:
            search_results = pd.read_sql_query("""
                SELECT title, summary, key_concepts, url 
                FROM articles 
                WHERE title LIKE ? OR summary LIKE ? OR key_concepts LIKE ?
                ORDER BY processed_date DESC
            """, conn, params=[f'%{search_term}%']*3)
            
            st.write(f"Found {len(search_results)} matching articles")
            
            for _, result in search_results.iterrows():
                with st.expander(result['title']):
                    st.write(result['summary'])
                    st.write("**Concepts:**", result['key_concepts'])
                    st.write(f"[Read full article]({result['url']})")

if __name__ == "__main__":
    main()
