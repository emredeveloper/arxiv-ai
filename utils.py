"""
Utility functions for the arXiv AI application.
"""
import re
import streamlit as st
from typing import List, Optional
from deep_translator import GoogleTranslator
from database import Database


# Regex pattern for GitHub links
GITHUB_PATTERN = r"https://github\.com/[a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+"


def extract_github_links(text: str) -> List[str]:
    """Extract GitHub repository links from text."""
    try:
        return re.findall(GITHUB_PATTERN, text)
    except Exception as e:
        st.error(f"GitHub link extraction error: {str(e)}")
        return []


def translate_text(text: str, dest_language: str = "tr", use_cache: bool = True) -> str:
    """
    Translate text to the specified language.
    
    Args:
        text: Text to translate
        dest_language: Target language code (default: 'tr' for Turkish)
        use_cache: Whether to use cached translations
    
    Returns:
        Translated text or original text if translation fails
    """
    if not text or not text.strip():
        return text
    
    try:
        # Check cache first if enabled
        if use_cache:
            db = Database()
            cached = db.get_translation(text, dest_language)
            if cached:
                return cached
        
        # Perform translation
        translator = GoogleTranslator(source='auto', target=dest_language)
        translated = translator.translate(text)
        
        # Save to cache if enabled
        if use_cache and translated:
            db = Database()
            db.save_translation(text, translated, source_lang='en', target_lang=dest_language)
        
        return translated
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return text


def format_authors(authors) -> str:
    """Format author list for display."""
    try:
        return ', '.join(author.name for author in authors)
    except Exception as e:
        st.error(f"Author formatting error: {str(e)}")
        return "Unknown Authors"


def format_date(date_obj) -> str:
    """Format datetime object to readable string."""
    try:
        return date_obj.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        st.error(f"Date formatting error: {str(e)}")
        return "Unknown Date"


def get_arxiv_id(entry_url: str) -> str:
    """Extract arXiv ID from entry URL."""
    try:
        # arXiv URLs are like: http://arxiv.org/abs/2301.12345v1
        match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', entry_url)
        if match:
            return match.group(1)
        return entry_url
    except Exception as e:
        st.error(f"arXiv ID extraction error: {str(e)}")
        return entry_url


def load_custom_css():
    """Load custom CSS styles for the application."""
    st.markdown(
        """
        <style>
        /* Card styling */
        .card {
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            background-color: #f8f9fa;
            border: 1px solid #e0e0e0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        .card h3 {
            color: #2c3e50;
            font-size: 20px;
            margin-top: 0;
            margin-bottom: 10px;
        }
        .card h5 {
            color: #34495e;
            font-size: 16px;
            margin-bottom: 5px;
        }
        
        /* Button styling */
        .stButton button {
            background-color: #3498db;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #2980b9;
        }
        
        /* Success message */
        .success-message {
            padding: 10px;
            border-radius: 5px;
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            margin: 10px 0;
        }
        
        /* Error message */
        .error-message {
            padding: 10px;
            border-radius: 5px;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            margin: 10px 0;
        }
        
        /* Info box */
        .info-box {
            padding: 15px;
            border-radius: 10px;
            background-color: #e7f3ff;
            border-left: 4px solid #2196F3;
            margin: 15px 0;
        }
        
        /* Stats card */
        .stats-card {
            padding: 15px;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            margin: 10px 0;
        }
        .stats-card h2 {
            margin: 0;
            font-size: 32px;
        }
        .stats-card p {
            margin: 5px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def show_success_message(message: str):
    """Display a success message."""
    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)


def show_error_message(message: str):
    """Display an error message."""
    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)


def show_info_box(message: str):
    """Display an info box."""
    st.markdown(f'<div class="info-box">ℹ️ {message}</div>', unsafe_allow_html=True)


def validate_date_range(start_date, end_date) -> bool:
    """Validate that start date is before end date."""
    try:
        return start_date <= end_date
    except Exception as e:
        st.error(f"Date validation error: {str(e)}")
        return False


def safe_execute(func, error_message: str = "An error occurred", default_return=None):
    """
    Safely execute a function with error handling.
    
    Args:
        func: Function to execute
        error_message: Message to display on error
        default_return: Default value to return on error
    
    Returns:
        Function result or default_return on error
    """
    try:
        return func()
    except Exception as e:
        st.error(f"{error_message}: {str(e)}")
        return default_return
