# app/core/insights.py
import sqlite3
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class InsightsManager:
    """Manages concept tracking and insight generation across articles"""
    
    def __init__(self, database):
        self.db = database
        self.logger = logging.getLogger(__name__)

    def track_concepts(self, article: Dict) -> None:
        """Track and connect concepts across articles"""
        try:
            if 'key_concepts' not in article:
                self.logger.warning(f"No key concepts found for article: {article.get('title', 'Unknown')}")
                return
                
            concepts = article['key_concepts'].split(',')
            current_time = datetime.now()
            
            with sqlite3.connect(self.db.db_path) as conn:
                for concept in concepts:
                    concept = concept.strip()
                    if concept:
                        conn.execute('''
                            INSERT INTO concepts (name, frequency, last_seen)
                            VALUES (?, 1, ?)
                            ON CONFLICT(name) DO UPDATE SET 
                            frequency = frequency + 1,
                            last_seen = excluded.last_seen
                        ''', (concept, current_time))
                conn.commit()
                
            self.logger.info(f"Tracked {len(concepts)} concepts for article: {article.get('title', 'Unknown')}")
            
        except Exception as e:
            self.logger.error(f"Error tracking concepts: {str(e)}")
            raise

    def get_related_content(self, concept: str) -> List[Dict]:
        """Find related articles by concept"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.execute('''
                    SELECT 
                        title,
                        summary,
                        insights,
                        published_date
                    FROM articles 
                    WHERE key_concepts LIKE ?
                    ORDER BY published_date DESC
                    LIMIT 5
                ''', (f'%{concept}%',))
                
                # Convert to list of dictionaries
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                self.logger.info(f"Found {len(results)} related articles for concept: {concept}")
                return results
                
        except Exception as e:
            self.logger.error(f"Error getting related content: {str(e)}")
            raise

    def get_trending_concepts(self, days: int = 7) -> List[Dict]:
        """Get trending concepts from recent articles"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.execute('''
                    SELECT 
                        name,
                        frequency,
                        last_seen
                    FROM concepts
                    WHERE last_seen >= datetime('now', ?)
                    ORDER BY frequency DESC
                    LIMIT 10
                ''', (f'-{days} days',))
                
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                
                self.logger.info(f"Retrieved {len(results)} trending concepts")
                return results
                
        except Exception as e:
            self.logger.error(f"Error getting trending concepts: {str(e)}")
            raise

    def get_concept_summary(self, concept: str) -> Dict:
        """Get a summary of a concept's appearances and insights"""
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                # Get concept details
                cursor = conn.execute('''
                    SELECT 
                        frequency,
                        last_seen
                    FROM concepts
                    WHERE name = ?
                ''', (concept,))
                
                concept_details = cursor.fetchone()
                
                if not concept_details:
                    return None
                    
                # Get related articles
                related_articles = self.get_related_content(concept)
                
                return {
                    'concept': concept,
                    'frequency': concept_details[0],
                    'last_seen': concept_details[1],
                    'related_articles': related_articles
                }
                
        except Exception as e:
            self.logger.error(f"Error getting concept summary: {str(e)}")
            raise

    def get_learning_recommendations(self) -> List[Dict]:
        """Generate learning recommendations based on tracked concepts"""
        try:
            trending = self.get_trending_concepts(days=7)
            recommendations = []
            
            for trend in trending:
                concept = trend['name']
                related = self.get_related_content(concept)
                
                if related:
                    recommendations.append({
                        'concept': concept,
                        'frequency': trend['frequency'],
                        'recommended_articles': related[:3]  # Top 3 related articles
                    })
                    
            self.logger.info(f"Generated {len(recommendations)} learning recommendations")
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {str(e)}")
            raise