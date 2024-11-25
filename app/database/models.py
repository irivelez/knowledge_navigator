from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class Content(Base):
    __tablename__ = 'content'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(500))
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(200))
    category = Column(String(100))
    url = Column(String(500))
    published_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Content(title={self.title}, source={self.source})>"

def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine