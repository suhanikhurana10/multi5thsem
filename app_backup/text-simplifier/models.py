"""
Data models for standardized input/output across all conversion modules.
"""
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class ConversionStatus(Enum):
    """Status of conversion attempt."""
    VALIDATED = "validated"      # Passed all validation checks
    FLAGGED = "flagged"           # Failed validation, needs manual review
    FAILED = "failed"             # Conversion failed entirely
    IN_PROGRESS = "in_progress"   # Currently processing

class FormatType(Enum):
    """Supported output formats."""
    SIMPLIFIED_TEXT = "simplified_text"
    AUDIO = "audio"
    BRAILLE = "braille"
    VISUAL_ENHANCED = "visual_enhanced"

@dataclass
class ValidationMetrics:
    """Validation metrics for converted content."""
    semantic_similarity: Optional[float] = None
    difficulty_change: Optional[float] = None
    semantic_pass: bool = False
    difficulty_pass: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'semantic_similarity': self.semantic_similarity,
            'difficulty_change': self.difficulty_change,
            'semantic_pass': self.semantic_pass,
            'difficulty_pass': self.difficulty_pass
        }

@dataclass
class ConversionResult:
    """Standardized result from any conversion module."""
    
    # Core fields
    status: ConversionStatus
    format_type: FormatType
    original_text: str
    converted_content: Any  # str for text, bytes for audio, etc.
    
    # Validation data
    metrics: ValidationMetrics
    iterations_taken: int
    
    # Optional fields
    error_message: Optional[str] = None
    warnings: Optional[list] = None
    file_path: Optional[str] = None  # Path to saved output file
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'status': self.status.value,
            'format_type': self.format_type.value,
            'original_text': self.original_text,
            'converted_content': self.converted_content,
            'metrics': self.metrics.to_dict(),
            'iterations_taken': self.iterations_taken,
            'error_message': self.error_message,
            'warnings': self.warnings or [],
            'file_path': self.file_path
        }
    
    @property
    def is_validated(self) -> bool:
        """Check if conversion passed validation."""
        return self.status == ConversionStatus.VALIDATED
    
    @property
    def needs_review(self) -> bool:
        """Check if conversion needs manual review."""
        return self.status == ConversionStatus.FLAGGED

@dataclass
class AssessmentItem:
    """Single assessment question/item to be converted."""
    
    id: str
    text: str
    has_math: bool = False
    difficulty_level: Optional[str] = None  # "easy", "medium", "hard"
    metadata: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'text': self.text,
            'has_math': self.has_math,
            'difficulty_level': self.difficulty_level,
            'metadata': self.metadata or {}
        }
