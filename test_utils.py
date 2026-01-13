"""
Unit tests for utility functions.
"""
import unittest
from utils import (
    extract_github_links,
    get_arxiv_id,
    format_authors,
    validate_date_range
)
from datetime import datetime, timedelta


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_extract_github_links(self):
        """Test GitHub link extraction."""
        text = """
        This paper presents a new method. 
        Code is available at https://github.com/user/repo
        and also at https://github.com/another/project
        """
        links = extract_github_links(text)
        self.assertEqual(len(links), 2)
        self.assertIn("https://github.com/user/repo", links)
        self.assertIn("https://github.com/another/project", links)
    
    def test_extract_github_links_no_links(self):
        """Test GitHub link extraction with no links."""
        text = "This paper has no GitHub links."
        links = extract_github_links(text)
        self.assertEqual(len(links), 0)
    
    def test_get_arxiv_id(self):
        """Test arXiv ID extraction from URL."""
        url = "http://arxiv.org/abs/2301.12345v1"
        arxiv_id = get_arxiv_id(url)
        self.assertEqual(arxiv_id, "2301.12345")
    
    def test_get_arxiv_id_invalid(self):
        """Test arXiv ID extraction with invalid URL."""
        url = "https://example.com/invalid"
        arxiv_id = get_arxiv_id(url)
        self.assertEqual(arxiv_id, url)  # Should return original URL
    
    def test_validate_date_range_valid(self):
        """Test date range validation with valid range."""
        start = datetime.now() - timedelta(days=7)
        end = datetime.now()
        self.assertTrue(validate_date_range(start, end))
    
    def test_validate_date_range_invalid(self):
        """Test date range validation with invalid range."""
        start = datetime.now()
        end = datetime.now() - timedelta(days=7)
        self.assertFalse(validate_date_range(start, end))
    
    def test_validate_date_range_equal(self):
        """Test date range validation with equal dates."""
        date = datetime.now()
        self.assertTrue(validate_date_range(date, date))


class MockAuthor:
    """Mock author object for testing."""
    def __init__(self, name):
        self.name = name


class TestFormatting(unittest.TestCase):
    """Test cases for formatting functions."""
    
    def test_format_authors(self):
        """Test author list formatting."""
        authors = [MockAuthor("John Doe"), MockAuthor("Jane Smith")]
        formatted = format_authors(authors)
        self.assertEqual(formatted, "John Doe, Jane Smith")
    
    def test_format_authors_single(self):
        """Test formatting single author."""
        authors = [MockAuthor("John Doe")]
        formatted = format_authors(authors)
        self.assertEqual(formatted, "John Doe")
    
    def test_format_authors_empty(self):
        """Test formatting empty author list."""
        authors = []
        formatted = format_authors(authors)
        self.assertEqual(formatted, "")


if __name__ == '__main__':
    unittest.main()
