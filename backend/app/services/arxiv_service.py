"""
arXiv API service with caching and error handling.
"""
import arxiv
from typing import List, Optional
from datetime import datetime
from ..schemas import ArticleBase


class ArxivService:
    """Service for interacting with arXiv API."""
    
    def __init__(self):
        self.client = arxiv.Client()
    
    async def search_articles(
        self,
        query: str = "cat:cs.LG",
        max_results: int = 10,
        sort_by: str = "Yeniden Eskiye"
    ) -> List[ArticleBase]:
        """
        Search articles from arXiv.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            sort_by: Sort order
        
        Returns:
            List of articles
        """
        try:
            sort_order = (
                arxiv.SortOrder.Descending 
                if sort_by == "Yeniden Eskiye" 
                else arxiv.SortOrder.Ascending
            )
            
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=sort_order
            )
            
            results = list(self.client.results(search))
            
            # Convert to ArticleBase schema
            articles = []
            for result in results:
                article = ArticleBase(
                    arxiv_id=self._extract_arxiv_id(result.entry_id),
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    summary=result.summary,
                    published_date=result.published.strftime("%Y-%m-%d %H:%M"),
                    entry_url=result.entry_id,
                    pdf_url=result.pdf_url,
                    github_links=self._extract_github_links(result.summary)
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            raise Exception(f"Error fetching articles: {str(e)}")
    
    async def search_by_category(
        self,
        category: str,
        max_results: int = 10
    ) -> List[ArticleBase]:
        """Search articles by category."""
        query = f"cat:{category}"
        return await self.search_articles(query, max_results)
    
    async def search_by_keyword(
        self,
        keyword: str,
        max_results: int = 10
    ) -> List[ArticleBase]:
        """Search articles by keyword."""
        try:
            search = arxiv.Search(
                query=keyword,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = list(self.client.results(search))
            
            articles = []
            for result in results:
                article = ArticleBase(
                    arxiv_id=self._extract_arxiv_id(result.entry_id),
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    summary=result.summary,
                    published_date=result.published.strftime("%Y-%m-%d %H:%M"),
                    entry_url=result.entry_id,
                    pdf_url=result.pdf_url,
                    github_links=self._extract_github_links(result.summary)
                )
                articles.append(article)
            
            return articles
            
        except Exception as e:
            raise Exception(f"Error searching by keyword: {str(e)}")
    
    def _extract_arxiv_id(self, entry_url: str) -> str:
        """Extract arXiv ID from entry URL."""
        import re
        match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', entry_url)
        return match.group(1) if match else entry_url
    
    def _extract_github_links(self, text: str) -> List[str]:
        """Extract GitHub links from text."""
        import re
        pattern = r"https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+"
        return re.findall(pattern, text)


# Singleton instance
arxiv_service = ArxivService()
