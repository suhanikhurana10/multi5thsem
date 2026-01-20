from fastapi import APIRouter
from pydantic import BaseModel

from app.preprocessor import preprocess_text
from app.tagger import tag_text
from app.braille_engine import convert_to_braille

router = APIRouter()

class ManualInput(BaseModel):
    content: str

@router.post("/convert-text")
def convert_text(data: ManualInput):
    raw_text = data.content

    cleaned_text = preprocess_text(raw_text)
    tagged_text = tag_text(cleaned_text)
    braille_file_path = convert_to_braille(tagged_text)

    return {
        "raw_text_preview": raw_text[:300],
        "cleaned_text_preview": cleaned_text[:300],
        "tagged_preview": tagged_text[:300],
        "braille_file_path": braille_file_path
    }
