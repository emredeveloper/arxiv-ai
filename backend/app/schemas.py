"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Article Schemas
class ArticleBase(BaseModel):
    """Base article schema."""
    arxiv_id: str
    title: str
    authors: List[str]
    summary: str
    published_date: str
    entry_url: str
    pdf_url: Optional[str] = None
    github_links: Optional[List[str]] = []


class ArticleResponse(ArticleBase):
    """Article response schema."""
    like_count: int = 0
    is_favorite: bool = False
    
    class Config:
        from_attributes = True


# Favorite Schemas
class FavoriteCreate(BaseModel):
    """Schema for creating a favorite."""
    arxiv_id: str
    title: str
    authors: List[str]
    summary: str
    published_date: str
    entry_url: str
    github_links: Optional[List[str]] = []
    category: str = "general"


class FavoriteResponse(BaseModel):
    """Favorite response schema."""
    id: int
    arxiv_id: str
    title: str
    authors: List[str]
    summary: str
    published_date: str
    entry_url: str
    github_links: List[str]
    category: str
    added_date: datetime
    
    class Config:
        from_attributes = True


# Like Schemas
class LikeResponse(BaseModel):
    """Like response schema."""
    arxiv_id: str
    like_count: int
    
    class Config:
        from_attributes = True


# Translation Schemas
class TranslationRequest(BaseModel):
    """Translation request schema."""
    text: str
    target_lang: str = "tr"
    source_lang: str = "en"


class TranslationResponse(BaseModel):
    """Translation response schema."""
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    cached: bool = False


# Search Schemas
class SearchParams(BaseModel):
    """Search parameters schema."""
    query: Optional[str] = "cat:cs.LG"
    max_results: int = Field(default=10, ge=1, le=100)
    sort_by: str = "Yeniden Eskiye"
    category: Optional[str] = None
    keyword: Optional[str] = None


# Statistics Schemas
class StatisticsResponse(BaseModel):
    """Statistics response schema."""
    total_favorites: int
    total_likes: int
    total_categories: int
    category_distribution: dict
    most_liked_articles: List[dict]


# Generic Response
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str
    success: bool = True
