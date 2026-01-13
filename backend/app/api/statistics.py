"""
Statistics API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from ..schemas import StatisticsResponse
from ..models import Favorite, Like

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    """
    Get application statistics.
    
    Returns statistics about favorites, likes, and categories.
    """
    try:
        # Total favorites
        total_favorites = db.query(func.count(Favorite.id)).scalar()
        
        # Total likes
        total_likes = db.query(func.sum(Like.like_count)).scalar() or 0
        
        # Category distribution
        category_counts = db.query(
            Favorite.category,
            func.count(Favorite.id)
        ).group_by(Favorite.category).all()
        
        category_distribution = {cat: count for cat, count in category_counts}
        total_categories = len(category_distribution)
        
        # Most liked articles
        favorites = db.query(Favorite).all()
        articles_with_likes = []
        
        for fav in favorites:
            like = db.query(Like).filter(Like.arxiv_id == fav.arxiv_id).first()
            if like and like.like_count > 0:
                articles_with_likes.append({
                    "title": fav.title,
                    "arxiv_id": fav.arxiv_id,
                    "like_count": like.like_count
                })
        
        # Sort by like count
        articles_with_likes.sort(key=lambda x: x['like_count'], reverse=True)
        most_liked = articles_with_likes[:5]
        
        return StatisticsResponse(
            total_favorites=total_favorites,
            total_likes=int(total_likes),
            total_categories=total_categories,
            category_distribution=category_distribution,
            most_liked_articles=most_liked
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
