from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, Optional

class ValidationStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"

@dataclass
class AssessmentItem:
    id: str
    text: str
    has_math: bool = False
    difficulty_level: str = "medium"

@dataclass
class ValidationMetrics:
    semantic_score: float
    difficulty_change: float
    preserves_math: bool = True
    concept_overlap: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "semantic_score": self.semantic_score,
            "difficulty_change": self.difficulty_change,
            "preserves_math": self.preserves_math,
            "concept_overlap": self.concept_overlap
        }


@dataclass
class ConversionResult:
    original_content: str
    converted_content: str
    status: ValidationStatus
    metrics: ValidationMetrics
    is_validated: bool
    needs_review: bool
    attempts: int = 1
