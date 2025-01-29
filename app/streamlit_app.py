# app/streamlit_app.py
import streamlit as st
from datetime import datetime
from database.models import Database
from core.processor import ContentProcessor

# Page configuration
st.set_page_config(
   page_title="Daily Tech Digest", 
   page_icon="📰",
   layout="wide"
)

# Custom CSS for a cleaner look
st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px;
            color: #6B7280;
            font-size: 14px;
            font-weight: 500;
            padding: 8px 16px;
        }
        .stTabs [aria-selected="true"] {
            background-color: #EEF2FF;
            color: #4F46E5;
        }
    </style>
""", unsafe_allow_html=True)

def main():
   # Initialize components
   db = Database()
   processor = ContentProcessor()
   
   # Header
   st.title("🗞️ Daily Tech Digest")
   st.subheader(f"Today's Tech News Summary - {datetime.now().strftime('%B %d, %Y')}")
   
   # Get today's articles
   articles = db.get_todays_articles()
   if not articles:
       st.info("Today's digest is being prepared. Please check back later.")
       return
       
   grouped_insights = processor.group_articles_by_topic(articles)
   
   # Stats row
   col1, col2, col3 = st.columns(3)
   with col1:
       st.metric("Articles", len(articles))
   with col2:
       st.metric("Sources", len(set(a['source'] for a in articles)))
   with col3:
       st.metric("Topics", len([g for g in grouped_insights.values() if g]))
   
   # Create tabs for different categories
   tabs = st.tabs([
       f"AI & ML 🤖 ({len(grouped_insights['AI_ML']['articles']) if grouped_insights['AI_ML'] else 0})",
       f"Business 💼 ({len(grouped_insights['Business']['articles']) if grouped_insights['Business'] else 0})",
       f"Cybersecurity 🔒 ({len(grouped_insights['Cybersecurity']['articles']) if grouped_insights['Cybersecurity'] else 0})",
       f"Innovation 🔬 ({len(grouped_insights['Innovation']['articles']) if grouped_insights['Innovation'] else 0})",
       f"Tech 💻 ({len(grouped_insights['Tech']['articles']) if grouped_insights['Tech'] else 0})"
   ])
   
   # Display articles in each tab
   for tab, (topic, insight) in zip(tabs, grouped_insights.items()):
       with tab:
           if insight:
               # Show topic insights
               st.markdown("### 🔍 Key Insights")
               if 'insights' in insight and insight['insights']:
                   for idx, insight_text in enumerate(insight['insights'], 1):
                       st.markdown(f"{idx}. {insight_text}")
               else:
                   st.markdown("No insights available for this topic.")
               
               st.markdown("### 📰 Articles")
               for article in insight['articles']:
                   with st.expander(f"📰 {article['title']}", expanded=False):
                       st.markdown(f"**Summary:**")
                       st.write(article['summary'])
                       
                       col1, col2 = st.columns([3,1])
                       with col1:
                           st.caption(f"Source: {article['source']}")
                       with col2:
                           st.markdown(f"[Read More →]({article['url']})")
                       
                       st.divider()
           else:
               st.info(f"No {topic} articles today.")

   # Footer
   st.markdown("---")
   st.caption("Updated daily with the latest tech news")

if __name__ == "__main__":
   main()