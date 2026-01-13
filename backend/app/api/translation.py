"""
Translation API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import TranslationRequest, TranslationResponse
from ..services.translation_service import translation_service

router = APIRouter(prefix="/translate", tags=["translation"])


@router.post("/", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    db: Session = Depends(get_db)
):
    """
    Translate text to target language.
    
    - **text**: Text to translate
    - **target_lang**: Target language code (default: tr)
    - **source_lang**: Source language code (default: en)
    """
    try:
        result = await translation_service.translate(db, request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
