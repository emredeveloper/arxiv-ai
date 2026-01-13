"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base


class Favorite(Base):
    """Favorite articles table."""
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)
    summary = Column(Text)
    published_date = Column(String)
    entry_url = Column(String)
    github_links = Column(JSON)
    category = Column(String, default="general")
    added_date = Column(DateTime(timezone=True), server_default=func.now())


class Like(Base):
    """Article likes table."""
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, unique=True, index=True, nullable=False)
    like_count = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Translation(Base):
    """Translation cache table."""
    __tablename__ = "translations"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    source_lang = Column(String, default="en")
    target_lang = Column(String, default="tr")
    created_date = Column(DateTime(timezone=True), server_default=func.now())


class UserInteraction(Base):
    """User interactions log table."""
    __tablename__ = "user_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    arxiv_id = Column(String, nullable=False, index=True)
    interaction_type = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
