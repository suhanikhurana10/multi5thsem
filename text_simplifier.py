"""
Text Simplification Module with Internal Validation
Part of: Adaptive Multi-Format Assessment Generator

Author: Aditi
Course: V Semester Experiential Learning (ACY 2025-26)
Project: SDG 4 Quality Education

This module:
1. Simplifies assessment text using Meta Llama 3.2 3B
2. Validates internally (semantic + difficulty)
3. Passes to adaptive regeneration if validation fails
4. Outputs to evidence dashboard if validation passes
"""

from huggingface_hub import InferenceClient
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Import models for compatibility
from models import AssessmentItem, ConversionResult, ValidationStatus, ValidationMetrics

# Load environment variables
load_dotenv()

class TextSimplifier:
    """
    Text simplification with built-in validation.
    Uses hybrid validation: internal checks first, then common validation if needed.
    """
    
    def __init__(self, hf_token: Optional[str] = None):
        """Initialize with Hugging Face token from environment or parameter"""
        self.hf_token = hf_token or os.getenv('HUGGINGFACE_API_KEY')
        
        # Initialize Llama model client
        if self.hf_token:
            self.client = InferenceClient(token=self.hf_token)
        else:
            print("WARNING: No HUGGINGFACE_API_KEY found. Simplification checks will fail.")
            self.client = None

        self.model_id = "meta-llama/Llama-3.2-3B-Instruct"
        
        # Import validators (these are INTERNAL to this module)
        from semantic_checker import SemanticChecker
        from difficulty_scorer import DifficultyScorer
        
        self.semantic_checker = SemanticChecker()
        self.difficulty_scorer = DifficultyScorer()
        
        # Validation thresholds
        self.SEMANTIC_THRESHOLD = 0.85
        self.DIFFICULTY_THRESHOLD = 10.0  # Max 10% change
        self.MAX_INTERNAL_ATTEMPTS = 3
    
    def simplify(
        self, 
        text: str, 
        preserve_math: bool = True,
        simplification_level: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Main simplification method with internal validation loop.
        
        Args:
            text: Original assessment question
            preserve_math: Whether to preserve mathematical notation
            simplification_level: "minimal", "moderate", or "significant"
            
        Returns:
            Dictionary with:
                - simplified_text: The simplified version
                - passed_internal_validation: True/False
                - semantic_score: Similarity score
                - difficulty_change: Percentage change in difficulty
                - needs_regeneration: True if failed and needs adaptive regeneration
                - metadata: Additional info
        """
        import sys
        
        print(f"\n{'='*80}", flush=True)
        print(f"TEXT SIMPLIFIER - Internal Validation Mode", flush=True)
        print(f"{'='*80}\n", flush=True)
        print(f"Input: {text[:100]}...", flush=True)
        
        # Calculate original difficulty
        original_difficulty = self.difficulty_scorer.calculate_difficulty(text)
        original_score = original_difficulty['composite_difficulty']
        print(f"Original Difficulty Score: {original_score}", flush=True)
        
        best_result = None
        best_validation_score = -1
        
        # Internal validation loop (max 3 attempts)
        for attempt in range(1, self.MAX_INTERNAL_ATTEMPTS + 1):
            print(f"\n[Attempt] Internal Attempt {attempt}/{self.MAX_INTERNAL_ATTEMPTS}", flush=True)
            
            # Generate simplified version
            if self.client:
                simplified = self._generate_simplified(
                    text, 
                    preserve_math, 
                    simplification_level,
                    attempt
                )
            else:
                simplified = None
                print("  [Error] No API Client available.")
            
            if not simplified:
                print("  [Failed] Generation failed")
                if not self.client: return self._create_failure_result(text, original_score, attempt)
                continue
            
            # Run internal validation
            validation = self._validate_internally(
                text, 
                simplified, 
                original_score
            )
            
            # Track best result
            difficulty_preservation = (100 - min(validation['difficulty_change'], 100)) / 100
            combined_score = (
                validation['semantic_score'] * 0.7 + 
                difficulty_preservation * 0.3
            )
            
            current_result = {
                'simplified_text': simplified,
                'passed_internal_validation': validation['passed'],
                'semantic_score': validation['semantic_score'],
                'difficulty_change': validation['difficulty_change'],
                'semantic_passed': validation['semantic_passed'],
                'difficulty_passed': validation['difficulty_passed'],
                'attempt': attempt,
                'needs_regeneration': False
            }

            if combined_score > best_validation_score:
                best_validation_score = combined_score
                best_result = current_result
            
            # If validation passed, return immediately
            if validation['passed']:
                print(f"\n[Passed] INTERNAL VALIDATION")
                print(f"   Semantic: {validation['semantic_score']:.3f} [OK]")
                print(f"   Difficulty: {validation['difficulty_change']:.1f}% change [OK]")
                print(f"\n[Evid] Sending to Evidence Dashboard\n")
                return best_result
        
        # If we're here, internal validation failed after all attempts
        print(f"\n[Failed] INTERNAL VALIDATION after {self.MAX_INTERNAL_ATTEMPTS} attempts")
        if best_result:
            print(f"   Best semantic: {best_result['semantic_score']:.3f}")
            print(f"   Best difficulty change: {best_result['difficulty_change']:.1f}%")
            best_result['needs_regeneration'] = True
            return best_result
        else:
             return self._create_failure_result(text, original_score, self.MAX_INTERNAL_ATTEMPTS)

    def _create_failure_result(self, text, original_score, attempt):
        return {
            'simplified_text': text, # Fallback to original
            'passed_internal_validation': False,
            'semantic_score': 1.0, # Exact match
            'difficulty_change': 0.0,
            'semantic_passed': True,
            'difficulty_passed': True,
            'attempt': attempt,
            'needs_regeneration': True
        }
    
    def _generate_simplified(
        self, 
        text: str, 
        preserve_math: bool,
        level: str,
        attempt: int
    ) -> str:
        """Generate simplified text using Llama 3.2"""
        from prompts import get_simplification_prompt
        
        # Adjust temperature based on attempt (more conservative each time)
        temperature = max(0.3, 0.7 - (attempt * 0.1))
        
        prompt = get_simplification_prompt(text, level, preserve_math)
        
        try:
            messages = [
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat_completion(
                messages,
                model=self.model_id,
                max_tokens=500,
                temperature=temperature,
                top_p=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  [Error] Generation error: {str(e)}")
            return None
    
    def _validate_internally(
        self, 
        original: str, 
        simplified: str, 
        original_difficulty_score: float
    ) -> Dict[str, Any]:
        """Run internal semantic and difficulty validation"""
        
        # Semantic similarity check
        semantic_score = self.semantic_checker.check_similarity(original, simplified)
        semantic_passed = semantic_score >= self.SEMANTIC_THRESHOLD
        
        # Difficulty change check
        simplified_difficulty = self.difficulty_scorer.calculate_difficulty(simplified)
        simplified_score = simplified_difficulty['composite_difficulty']
        
        difficulty_change = (
            abs(simplified_score - original_difficulty_score) / original_difficulty_score * 100
            if original_difficulty_score > 0 else 0
        )
        difficulty_passed = difficulty_change <= self.DIFFICULTY_THRESHOLD
        
        # Overall pass/fail
        passed = semantic_passed and difficulty_passed
        
        print(f"  [Metric] Semantic: {semantic_score:.3f} {'[OK]' if semantic_passed else '[FAIL] (threshold: 0.85)'}")
        print(f"  [Metric] Difficulty: {difficulty_change:.1f}% change {'[OK]' if difficulty_passed else '[FAIL] (max: 10%)'}")
        
        return {
            'semantic_score': semantic_score,
            'semantic_passed': semantic_passed,
            'difficulty_change': difficulty_change,
            'difficulty_passed': difficulty_passed,
            'passed': passed
        }
    
    def get_validation_summary(self, result: Dict[str, Any]) -> str:
        """Generate human-readable validation summary for dashboard"""
        status = "✅ PASSED" if result['passed_internal_validation'] else "⚠️ NEEDS REGENERATION"
        
        summary = f"""
Text Simplification Result
{'-' * 40}
Status: {status}
Semantic Similarity: {result.get('semantic_score', 0):.3f} / 0.85
Difficulty Change: {result.get('difficulty_change', 0):.1f}% / 10.0%
Attempts Used: {result.get('attempt', 0)}
{'→ Ready for Dashboard' if not result.get('needs_regeneration', False) else '→ Sent to Adaptive Regeneration'}
"""
        return summary

    def convert(self, item: AssessmentItem, **kwargs) -> ConversionResult:
        """Standardized interface method"""
        result = self.simplify(
            item.text, 
            simplification_level=kwargs.get("simplification_level", "moderate"),
            preserve_math=kwargs.get("preserve_math", item.has_math)
        )
        
        status = ValidationStatus.PASSED if result["passed_internal_validation"] else ValidationStatus.NEEDS_REVIEW
        
        # Construct metrics object
        metrics = ValidationMetrics(
            semantic_score=result["semantic_score"],
            difficulty_change=result["difficulty_change"],
            preserves_math=kwargs.get("preserve_math", item.has_math),
            concept_overlap=0.0 # Not calculated in new module yet, defaulting
        )

        return ConversionResult(
            original_content=item.text,
            converted_content=result["simplified_text"],
            status=status,
            metrics=metrics,
            is_validated=result["passed_internal_validation"],
            needs_review=result.get("needs_regeneration", False),
            attempts=result["attempt"]
        )
