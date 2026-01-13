"""
Favorites API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas import FavoriteCreate, FavoriteResponse, MessageResponse
from ..models import Favorite, UserInteraction

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("/", response_model=List[FavoriteResponse])
def get_favorites(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all favorite articles.
    
    - **category**: Optional category filter
    """
    try:
        query = db.query(Favorite)
        if category:
            query = query.filter(Favorite.category == category)
        
        favorites = query.order_by(Favorite.added_date.desc()).all()
        return favorites
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=FavoriteResponse)
def add_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db)
):
    """
    Add an article to favorites.
    """
    try:
        # Check if already exists
        existing = db.query(Favorite).filter(
            Favorite.arxiv_id == favorite.arxiv_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Article already in favorites")
        
        # Create new favorite
        db_favorite = Favorite(**favorite.model_dump())
        db.add(db_favorite)
        
        # Log interaction
        interaction = UserInteraction(
            arxiv_id=favorite.arxiv_id,
            interaction_type="favorite"
        )
        db.add(interaction)
        
        db.commit()
        db.refresh(db_favorite)
        
        return db_favorite
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{arxiv_id}", response_model=MessageResponse)
def remove_favorite(
    arxiv_id: str,
    db: Session = Depends(get_db)
):
    """
    Remove an article from favorites.
    
    - **arxiv_id**: arXiv article ID
    """
    try:
        favorite = db.query(Favorite).filter(
            Favorite.arxiv_id == arxiv_id
        ).first()
        
        if not favorite:
            raise HTTPException(status_code=404, detail="Favorite not found")
        
        db.delete(favorite)
        
        # Log interaction
        interaction = UserInteraction(
            arxiv_id=arxiv_id,
            interaction_type="unfavorite"
        )
        db.add(interaction)
        
        db.commit()
        
        return MessageResponse(message="Favorite removed successfully")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/check/{arxiv_id}")
def check_favorite(
    arxiv_id: str,
    db: Session = Depends(get_db)
):
    """
    Check if an article is in favorites.
    
    - **arxiv_id**: arXiv article ID
    """
    try:
        favorite = db.query(Favorite).filter(
            Favorite.arxiv_id == arxiv_id
        ).first()
        
        return {"is_favorite": favorite is not None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
