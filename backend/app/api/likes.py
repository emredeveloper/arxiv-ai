"""
Likes API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import LikeResponse
from ..models import Like, UserInteraction

router = APIRouter(prefix="/likes", tags=["likes"])


@router.post("/{arxiv_id}", response_model=LikeResponse)
def add_like(
    arxiv_id: str,
    db: Session = Depends(get_db)
):
    """
    Add a like to an article.
    
    - **arxiv_id**: arXiv article ID
    """
    try:
        # Get or create like record
        like = db.query(Like).filter(Like.arxiv_id == arxiv_id).first()
        
        if like:
            like.like_count += 1
        else:
            like = Like(arxiv_id=arxiv_id, like_count=1)
            db.add(like)
        
        # Log interaction
        interaction = UserInteraction(
            arxiv_id=arxiv_id,
            interaction_type="like"
        )
        db.add(interaction)
        
        db.commit()
        db.refresh(like)
        
        return LikeResponse(arxiv_id=like.arxiv_id, like_count=like.like_count)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{arxiv_id}", response_model=LikeResponse)
def get_like_count(
    arxiv_id: str,
    db: Session = Depends(get_db)
):
    """
    Get like count for an article.
    
    - **arxiv_id**: arXiv article ID
    """
    try:
        like = db.query(Like).filter(Like.arxiv_id == arxiv_id).first()
        
        if not like:
            return LikeResponse(arxiv_id=arxiv_id, like_count=0)
        
        return LikeResponse(arxiv_id=like.arxiv_id, like_count=like.like_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
