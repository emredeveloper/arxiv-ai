"""
Translation service with caching.
"""
from deep_translator import GoogleTranslator
from sqlalchemy.orm import Session
from typing import Optional
from ..models import Translation
from ..schemas import TranslationRequest, TranslationResponse


class TranslationService:
    """Service for text translation with caching."""
    
    async def translate(
        self,
        db: Session,
        request: TranslationRequest
    ) -> TranslationResponse:
        """
        Translate text with caching.
        
        Args:
            db: Database session
            request: Translation request
        
        Returns:
            Translation response
        """
        # Check cache first
        cached = db.query(Translation).filter(
            Translation.original_text == request.text,
            Translation.target_lang == request.target_lang
        ).first()
        
        if cached:
            return TranslationResponse(
                original_text=cached.original_text,
                translated_text=cached.translated_text,
                source_lang=cached.source_lang,
                target_lang=cached.target_lang,
                cached=True
            )
        
        # Perform translation
        try:
            translator = GoogleTranslator(
                source=request.source_lang,
                target=request.target_lang
            )
            translated_text = translator.translate(request.text)
            
            # Save to cache
            translation = Translation(
                original_text=request.text,
                translated_text=translated_text,
                source_lang=request.source_lang,
                target_lang=request.target_lang
            )
            db.add(translation)
            db.commit()
            
            return TranslationResponse(
                original_text=request.text,
                translated_text=translated_text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                cached=False
            )
            
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")


# Singleton instance
translation_service = TranslationService()
