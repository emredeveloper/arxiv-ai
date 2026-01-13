"""
Articles API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas import ArticleResponse, SearchParams
from ..services.arxiv_service import arxiv_service
from ..models import Like

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=List[ArticleResponse])
async def get_articles(
    query: str = Query("cat:cs.LG", description="Search query"),
    max_results: int = Query(10, ge=1, le=100),
    sort_by: str = Query("Yeniden Eskiye"),
    db: Session = Depends(get_db)
):
    """
    Get articles from arXiv.
    
    - **query**: Search query (default: cat:cs.LG)
    - **max_results**: Maximum number of results (1-100)
    - **sort_by**: Sort order (Yeniden Eskiye or Eskiden Yeniye)
    """
    try:
        articles = await arxiv_service.search_articles(query, max_results, sort_by)
        
        # Enrich with like counts
        response = []
        for article in articles:
            like = db.query(Like).filter(Like.arxiv_id == article.arxiv_id).first()
            article_dict = article.model_dump()
            article_dict['like_count'] = like.like_count if like else 0
            response.append(ArticleResponse(**article_dict))
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category}", response_model=List[ArticleResponse])
async def get_articles_by_category(
    category: str,
    max_results: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get articles by category.
    
    - **category**: arXiv category (e.g., cs.LG, cs.AI, cs.CV)
    - **max_results**: Maximum number of results
    """
    try:
        articles = await arxiv_service.search_by_category(category, max_results)
        
        response = []
        for article in articles:
            like = db.query(Like).filter(Like.arxiv_id == article.arxiv_id).first()
            article_dict = article.model_dump()
            article_dict['like_count'] = like.like_count if like else 0
            response.append(ArticleResponse(**article_dict))
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search", response_model=List[ArticleResponse])
async def search_articles_by_keyword(
    keyword: str = Query(..., description="Search keyword"),
    max_results: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Search articles by keyword.
    
    - **keyword**: Search keyword
    - **max_results**: Maximum number of results
    """
    try:
        articles = await arxiv_service.search_by_keyword(keyword, max_results)
        
        response = []
        for article in articles:
            like = db.query(Like).filter(Like.arxiv_id == article.arxiv_id).first()
            article_dict = article.model_dump()
            article_dict['like_count'] = like.like_count if like else 0
            response.append(ArticleResponse(**article_dict))
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
