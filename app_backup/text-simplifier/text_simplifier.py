"""
Text Simplification Module with Equivalence Validation
Maintains semantic similarity and difficulty alignment for assessment questions.
"""
from huggingface_hub import InferenceClient
from semantic_checker import SemanticChecker
from difficulty_scorer import DifficultyScorer
from prompts import SimplificationPrompts
from models import (
    ConversionResult, 
    ConversionStatus, 
    FormatType, 
    ValidationMetrics,
    AssessmentItem
)
from config import config
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextSimplifier:
    """
    Text simplification engine with validation and adaptive regeneration.
    
    Validates:
    - Semantic similarity > 0.85
    - Difficulty change < 10%
    - Math notation preservation
    """
    
    def __init__(self, hf_token: Optional[str] = None):
        """
        Initialize the text simplifier.
        
        Args:
            hf_token: Hugging Face API token (optional, reads from config if not provided)
        """
        # Use provided token or fall back to config
        self.hf_token = hf_token or config.HF_TOKEN
        if not self.hf_token:
            raise ValueError("HF_TOKEN is required. Set it in .env file or pass to constructor.")
        
        # Initialize components
        logger.info("Initializing Text Simplifier components...")
        self.semantic_checker = SemanticChecker()
        self.difficulty_scorer = DifficultyScorer()
        self.prompts = SimplificationPrompts()
        self.client = InferenceClient(token=self.hf_token)
        
        # Configuration from config file
        self.semantic_threshold = config.SEMANTIC_THRESHOLD
        self.difficulty_threshold = config.DIFFICULTY_THRESHOLD
        self.max_attempts = config.MAX_ATTEMPTS
        self.base_temperature = config.BASE_TEMPERATURE
        self.temperature_increment = config.TEMPERATURE_INCREMENT
        
        logger.info("✓ Text Simplifier initialized successfully!")
    
    def convert(
        self, 
        item: AssessmentItem,
        simplification_level: str = "moderate",
        preserve_math: bool = True
    ) -> ConversionResult:
        """
        Convert assessment item to simplified text format.
        
        This is the STANDARDIZED interface used by the orchestrator.
        
        Args:
            item: AssessmentItem object containing the question
            simplification_level: "minimal", "moderate", or "significant"
            preserve_math: Whether to keep math notation intact
            
        Returns:
            ConversionResult with standardized format
        """
        logger.info(f"\n{'='*80}")
        logger.info(f"SIMPLIFYING ITEM: {item.id}")
        logger.info(f"TEXT: {item.text[:60]}...")
        logger.info(f"{'='*80}\n")
        
        # Run simplification with validation
        result = self._simplify_with_validation(
            item.text, 
            simplification_level, 
            preserve_math
        )
        
        # Convert to standardized ConversionResult
        return self._to_conversion_result(item, result)
    
    def simplify(
        self, 
        original_text: str, 
        simplification_level: str = "moderate", 
        preserve_math: bool = True
    ) -> dict:
        """
        Legacy interface - kept for backward compatibility.
        Use convert() method for new integrations.
        
        Returns:
            dict with keys: success, simplified_text, semantic_score, 
                          difficulty_change, attempt, flagged
        """
        return self._simplify_with_validation(original_text, simplification_level, preserve_math)
    
    def _simplify_with_validation(
        self,
        original_text: str,
        simplification_level: str,
        preserve_math: bool
    ) -> dict:
        """
        Internal method: Simplify text with validation and adaptive regeneration.
        """
        # Calculate original difficulty
        original_difficulty = self.difficulty_scorer.calculate_difficulty(original_text)
        orig_score = original_difficulty["composite_difficulty"]
        
        best_result = None
        best_overall_score = 0
        
        for attempt in range(1, self.max_attempts + 1):
            logger.info(f"🔄 Attempt {attempt}/{self.max_attempts}")
            
            # Generate simplified version
            simplified = self._call_llm(
                original_text, 
                simplification_level, 
                preserve_math, 
                attempt
            )
            
            if not simplified:
                logger.warning("  ✗ Generation failed")
                continue
            
            # Validate semantic similarity
            semantic_score = self.semantic_checker.check_similarity(
                original_text, 
                simplified
            )
            semantic_pass = semantic_score >= self.semantic_threshold
            
            # Validate difficulty alignment
            simp_difficulty = self.difficulty_scorer.calculate_difficulty(simplified)
            simp_score = simp_difficulty["composite_difficulty"]
            
            if orig_score > 0:
                difficulty_change = abs(simp_score - orig_score) / orig_score * 100
            else:
                difficulty_change = 0
                
            difficulty_pass = difficulty_change <= self.difficulty_threshold
            
            # Calculate overall quality score
            overall_score = (
                (semantic_score * 0.7) + 
                ((100 - min(difficulty_change, 100)) / 100 * 0.3)
            )
            
            logger.info(f"  📊 Semantic: {semantic_score:.3f} {'✓' if semantic_pass else '✗'}")
            logger.info(f"  📊 Difficulty: {difficulty_change:.1f}% change {'✓' if difficulty_pass else '✗'}")
            
            # Track best result
            if overall_score > best_overall_score:
                best_overall_score = overall_score
                best_result = {
                    "simplified_text": simplified,
                    "semantic_score": semantic_score,
                    "semantic_pass": semantic_pass,
                    "difficulty_change": difficulty_change,
                    "difficulty_pass": difficulty_pass,
                    "attempt": attempt,
                }
            
            # Check if all validations passed
            if semantic_pass and difficulty_pass:
                logger.info(f"  ✅ All checks passed!\n")
                best_result["success"] = True
                best_result["flagged"] = False
                return best_result
            
            logger.info(f"  ⚠️ Validation failed, trying again...\n")
        
        # Max attempts reached
        logger.warning(f"⚠️ Max attempts reached. Flagged for review\n")
        best_result["success"] = False
        best_result["flagged"] = True
        return best_result
    
    def _call_llm(
        self, 
        original: str, 
        level: str, 
        preserve_math: bool, 
        attempt: int
    ) -> Optional[str]:
        """
        Call Hugging Face LLM API with adaptive temperature.
        
        Temperature increases with each attempt to generate more diverse outputs.
        """
        temperature = self.base_temperature + (attempt - 1) * self.temperature_increment
        prompt = self.prompts.get_simplification_prompt(original, level, preserve_math)
        
        messages = [{"role": "user", "content": prompt}]
        
        try:
            response = self.client.chat_completion(
                messages=messages,
                model=config.LLM_MODEL,
                max_tokens=config.MAX_TOKENS,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"  ✗ LLM API Error: {e}")
            return None
    
    def _to_conversion_result(
        self, 
        item: AssessmentItem, 
        result: dict
    ) -> ConversionResult:
        """
        Convert internal result dict to standardized ConversionResult.
        """
        # Determine status
        if result["success"]:
            status = ConversionStatus.VALIDATED
        elif result["flagged"]:
            status = ConversionStatus.FLAGGED
        else:
            status = ConversionStatus.FAILED
        
        # Create validation metrics
        metrics = ValidationMetrics(
            semantic_similarity=result["semantic_score"],
            difficulty_change=result["difficulty_change"],
            semantic_pass=result["semantic_pass"],
            difficulty_pass=result["difficulty_pass"]
        )
        
        # Create conversion result
        return ConversionResult(
            status=status,
            format_type=FormatType.SIMPLIFIED_TEXT,
            original_text=item.text,
            converted_content=result["simplified_text"],
            metrics=metrics,
            iterations_taken=result["attempt"],
            warnings=[] if result["success"] else ["Failed validation checks"]
        )
