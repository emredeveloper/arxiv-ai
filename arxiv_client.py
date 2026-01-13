"""
arXiv API client module with error handling and caching.
"""
import streamlit as st
import arxiv
from typing import List, Optional
from datetime import datetime


class ArxivClient:
    """Wrapper for arXiv API with error handling."""
    
    def __init__(self):
        """Initialize the arXiv client."""
        self.client = arxiv.Client()
    
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def fetch_articles(_self, query: str, max_results: int, 
                       sort_by: str, start_date: Optional[datetime] = None,
                       end_date: Optional[datetime] = None) -> List:
        """
        Fetch articles from arXiv with error handling.
        
        Args:
            query: Search query (e.g., 'cat:cs.LG')
            max_results: Maximum number of results to fetch
            sort_by: Sort order ('Yeniden Eskiye' or 'Eskiden Yeniye')
            start_date: Filter articles after this date
            end_date: Filter articles before this date
        
        Returns:
            List of arXiv articles
        """
        try:
            sort_order = (arxiv.SortOrder.Descending if sort_by == "Yeniden Eskiye" 
                         else arxiv.SortOrder.Ascending)
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=sort_order
            )
            
            articles = list(_self.client.results(search))
            
            # Filter by date range if provided
            if start_date and end_date:
                articles = [
                    article for article in articles 
                    if start_date.date() <= article.published.date() <= end_date.date()
                ]
            
            return articles
            
        except arxiv.ArxivError as e:
            st.error(f"arXiv API Error: {str(e)}")
            return []
        except Exception as e:
            st.error(f"Error fetching articles: {str(e)}")
            return []
    
    def search_by_category(self, category: str, max_results: int = 10, 
                          sort_by: str = "Yeniden Eskiye") -> List:
        """
        Search articles by category.
        
        Args:
            category: arXiv category (e.g., 'cs.LG', 'cs.AI')
            max_results: Maximum number of results
            sort_by: Sort order
        
        Returns:
            List of articles
        """
        query = f"cat:{category}"
        return self.fetch_articles(query, max_results, sort_by)
    
    def search_by_keyword(self, keyword: str, max_results: int = 10,
                         sort_by: str = "Yeniden Eskiye") -> List:
        """
        Search articles by keyword.
        
        Args:
            keyword: Search keyword
            max_results: Maximum number of results
            sort_by: Sort order
        
        Returns:
            List of articles
        """
        try:
            sort_order = (arxiv.SortOrder.Descending if sort_by == "Yeniden Eskiye" 
                         else arxiv.SortOrder.Ascending)
            
            search = arxiv.Search(
                query=keyword,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance,
                sort_order=sort_order
            )
            
            return list(self.client.results(search))
            
        except Exception as e:
            st.error(f"Error searching by keyword: {str(e)}")
            return []
    
    def get_article_by_id(self, arxiv_id: str):
        """
        Get a specific article by its arXiv ID.
        
        Args:
            arxiv_id: arXiv article ID
        
        Returns:
            Article object or None
        """
        try:
            search = arxiv.Search(id_list=[arxiv_id])
            results = list(self.client.results(search))
            return results[0] if results else None
        except Exception as e:
            st.error(f"Error fetching article {arxiv_id}: {str(e)}")
            return None
