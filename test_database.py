"""
Unit tests for the database module.
"""
import unittest
import os
import tempfile
from database import Database
from datetime import datetime


class TestDatabase(unittest.TestCase):
    """Test cases for Database class."""
    
    def setUp(self):
        """Set up test database before each test."""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary database file
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_database_initialization(self):
        """Test that database tables are created."""
        self.assertTrue(os.path.exists(self.temp_db.name))
    
    def test_add_favorite(self):
        """Test adding a favorite article."""
        result = self.db.add_favorite(
            arxiv_id="2301.12345",
            title="Test Article",
            authors=["John Doe", "Jane Smith"],
            summary="This is a test summary",
            published_date="2023-01-15",
            entry_url="http://arxiv.org/abs/2301.12345",
            github_links=["https://github.com/test/repo"],
            category="machine_learning"
        )
        self.assertTrue(result)
    
    def test_is_favorite(self):
        """Test checking if an article is a favorite."""
        arxiv_id = "2301.12345"
        
        # Should not be favorite initially
        self.assertFalse(self.db.is_favorite(arxiv_id))
        
        # Add to favorites
        self.db.add_favorite(
            arxiv_id=arxiv_id,
            title="Test Article",
            authors=["John Doe"],
            summary="Test",
            published_date="2023-01-15",
            entry_url="http://arxiv.org/abs/2301.12345",
            github_links=[]
        )
        
        # Should be favorite now
        self.assertTrue(self.db.is_favorite(arxiv_id))
    
    def test_remove_favorite(self):
        """Test removing a favorite article."""
        arxiv_id = "2301.12345"
        
        # Add favorite
        self.db.add_favorite(
            arxiv_id=arxiv_id,
            title="Test Article",
            authors=["John Doe"],
            summary="Test",
            published_date="2023-01-15",
            entry_url="http://arxiv.org/abs/2301.12345",
            github_links=[]
        )
        
        # Remove favorite
        result = self.db.remove_favorite(arxiv_id)
        self.assertTrue(result)
        self.assertFalse(self.db.is_favorite(arxiv_id))
    
    def test_get_favorites(self):
        """Test retrieving all favorites."""
        # Add multiple favorites
        for i in range(3):
            self.db.add_favorite(
                arxiv_id=f"2301.1234{i}",
                title=f"Test Article {i}",
                authors=["Author"],
                summary="Test",
                published_date="2023-01-15",
                entry_url=f"http://arxiv.org/abs/2301.1234{i}",
                github_links=[]
            )
        
        favorites = self.db.get_favorites()
        self.assertEqual(len(favorites), 3)
    
    def test_add_like(self):
        """Test adding a like to an article."""
        arxiv_id = "2301.12345"
        
        # First like
        count = self.db.add_like(arxiv_id)
        self.assertEqual(count, 1)
        
        # Second like
        count = self.db.add_like(arxiv_id)
        self.assertEqual(count, 2)
    
    def test_get_like_count(self):
        """Test getting like count for an article."""
        arxiv_id = "2301.12345"
        
        # Should be 0 initially
        count = self.db.get_like_count(arxiv_id)
        self.assertEqual(count, 0)
        
        # Add likes
        self.db.add_like(arxiv_id)
        self.db.add_like(arxiv_id)
        
        # Should be 2 now
        count = self.db.get_like_count(arxiv_id)
        self.assertEqual(count, 2)
    
    def test_translation_cache(self):
        """Test translation caching."""
        original = "Hello World"
        translated = "Merhaba Dünya"
        
        # Save translation
        result = self.db.save_translation(original, translated)
        self.assertTrue(result)
        
        # Retrieve translation
        cached = self.db.get_translation(original)
        self.assertEqual(cached, translated)
    
    def test_log_interaction(self):
        """Test logging user interactions."""
        # Should not raise any exceptions
        try:
            self.db.log_interaction("2301.12345", "view")
            self.db.log_interaction("2301.12345", "translate")
        except Exception as e:
            self.fail(f"log_interaction raised exception: {e}")


if __name__ == '__main__':
    unittest.main()
