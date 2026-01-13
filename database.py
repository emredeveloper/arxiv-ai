"""
Database module for managing favorites and user interactions.
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os


class Database:
    """SQLite database handler for the arXiv AI application."""
    
    def __init__(self, db_path: str = "arxiv_ai.db"):
        """Initialize database connection and create tables if they don't exist."""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create database tables if they don't exist."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Favorites table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    arxiv_id TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    summary TEXT,
                    published_date TEXT,
                    entry_url TEXT,
                    github_links TEXT,
                    added_date TEXT NOT NULL,
                    category TEXT DEFAULT 'general'
                )
            """)
            
            # Likes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS likes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    arxiv_id TEXT UNIQUE NOT NULL,
                    like_count INTEGER DEFAULT 0,
                    last_updated TEXT NOT NULL
                )
            """)
            
            # User interactions table (for tracking user behavior)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    arxiv_id TEXT NOT NULL,
                    interaction_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # Translations cache table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    source_lang TEXT DEFAULT 'en',
                    target_lang TEXT DEFAULT 'tr',
                    created_date TEXT NOT NULL,
                    UNIQUE(original_text, target_lang)
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            raise Exception(f"Database initialization failed: {str(e)}")
    
    # Favorites operations
    def add_favorite(self, arxiv_id: str, title: str, authors: List[str], 
                     summary: str, published_date: str, entry_url: str, 
                     github_links: List[str], category: str = "general") -> bool:
        """Add an article to favorites."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO favorites 
                (arxiv_id, title, authors, summary, published_date, entry_url, 
                 github_links, added_date, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                arxiv_id,
                title,
                json.dumps(authors),
                summary,
                published_date,
                entry_url,
                json.dumps(github_links),
                datetime.now().isoformat(),
                category
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding favorite: {str(e)}")
            return False
    
    def remove_favorite(self, arxiv_id: str) -> bool:
        """Remove an article from favorites."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM favorites WHERE arxiv_id = ?", (arxiv_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error removing favorite: {str(e)}")
            return False
    
    def get_favorites(self, category: Optional[str] = None) -> List[Dict]:
        """Get all favorite articles, optionally filtered by category."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT * FROM favorites WHERE category = ? ORDER BY added_date DESC
                """, (category,))
            else:
                cursor.execute("SELECT * FROM favorites ORDER BY added_date DESC")
            
            rows = cursor.fetchall()
            conn.close()
            
            favorites = []
            for row in rows:
                favorites.append({
                    'id': row[0],
                    'arxiv_id': row[1],
                    'title': row[2],
                    'authors': json.loads(row[3]),
                    'summary': row[4],
                    'published_date': row[5],
                    'entry_url': row[6],
                    'github_links': json.loads(row[7]),
                    'added_date': row[8],
                    'category': row[9]
                })
            
            return favorites
        except Exception as e:
            print(f"Error getting favorites: {str(e)}")
            return []
    
    def is_favorite(self, arxiv_id: str) -> bool:
        """Check if an article is in favorites."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM favorites WHERE arxiv_id = ?", (arxiv_id,))
            count = cursor.fetchone()[0]
            
            conn.close()
            return count > 0
        except Exception as e:
            print(f"Error checking favorite: {str(e)}")
            return False
    
    # Likes operations
    def add_like(self, arxiv_id: str) -> int:
        """Add a like to an article and return the new like count."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO likes (arxiv_id, like_count, last_updated)
                VALUES (?, 1, ?)
                ON CONFLICT(arxiv_id) DO UPDATE SET
                    like_count = like_count + 1,
                    last_updated = ?
            """, (arxiv_id, datetime.now().isoformat(), datetime.now().isoformat()))
            
            cursor.execute("SELECT like_count FROM likes WHERE arxiv_id = ?", (arxiv_id,))
            like_count = cursor.fetchone()[0]
            
            conn.commit()
            conn.close()
            return like_count
        except Exception as e:
            print(f"Error adding like: {str(e)}")
            return 0
    
    def get_like_count(self, arxiv_id: str) -> int:
        """Get the like count for an article."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT like_count FROM likes WHERE arxiv_id = ?", (arxiv_id,))
            result = cursor.fetchone()
            
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error getting like count: {str(e)}")
            return 0
    
    # User interactions
    def log_interaction(self, arxiv_id: str, interaction_type: str):
        """Log a user interaction."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO user_interactions (arxiv_id, interaction_type, timestamp)
                VALUES (?, ?, ?)
            """, (arxiv_id, interaction_type, datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error logging interaction: {str(e)}")
    
    # Translation cache
    def get_translation(self, original_text: str, target_lang: str = "tr") -> Optional[str]:
        """Get a cached translation."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT translated_text FROM translations 
                WHERE original_text = ? AND target_lang = ?
            """, (original_text, target_lang))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting translation: {str(e)}")
            return None
    
    def save_translation(self, original_text: str, translated_text: str, 
                        source_lang: str = "en", target_lang: str = "tr") -> bool:
        """Save a translation to cache."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO translations 
                (original_text, translated_text, source_lang, target_lang, created_date)
                VALUES (?, ?, ?, ?, ?)
            """, (original_text, translated_text, source_lang, target_lang, 
                  datetime.now().isoformat()))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving translation: {str(e)}")
            return False
    
    def clear_old_translations(self, days: int = 30):
        """Clear translations older than specified days."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            cursor.execute("DELETE FROM translations WHERE created_date < ?", (cutoff_date,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error clearing old translations: {str(e)}")
