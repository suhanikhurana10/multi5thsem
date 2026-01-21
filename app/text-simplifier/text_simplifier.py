"""
Text Simplifier Module
Converts complex assessment text to simplified versions with validation
Now includes DEMO MODE for teammates without API keys
"""

import requests
import time
from typing import Optional
from models import AssessmentItem, ConversionResult
from semantic_checker import SemanticChecker
from difficulty_scorer import DifficultyScorer
from prompts import get_simplification_prompt
import config

class TextSimplifier:
    """Text simplification with equivalence validation"""
    
    def __init__(self):
        self.semantic_checker = SemanticChecker()
        self.difficulty_scorer = DifficultyScorer()
        self.headers = {
            "Authorization": f"Bearer {config.HUGGINGFACE_API_KEY}"
        } if config.HUGGINGFACE_API_KEY else {}
        
        # Check if running in demo mode
        self.demo_mode = not config.HUGGINGFACE_API_KEY
        
        if self.demo_mode:
            print("🎭 Running in DEMO MODE (no API key detected)")
            print("   Using sample simplified outputs for testing")
            print()
    
    def _generate_demo_output(self, text: str) -> str:
        """Generate demo simplified text when API key is not available"""
        
        # Simple rule-based simplification for demo
        simplified = text
        
        # Replace complex words with simpler ones
        replacements = {
            "evaluate": "find",
            "definite integral": "area under the curve",
            "determine": "find",
            "analyze": "look at",
            "relationship between": "connection between",
            "photosynthesis": "how plants make food",
            "cellular respiration": "how cells use energy",
            "perimeter": "distance around",
            "rectangular": "rectangle-shaped",
            "dimensions": "measurements"
        }
        
        for complex_word, simple_word in replacements.items():
            simplified = simplified.replace(complex_word, simple_word)
        
        return simplified
    
    def _call_llm_api(self, prompt: str) -> Optional[str]:
        """Call Hugging Face API or return demo output"""
        
        if self.demo_mode:
            # Extract original text from prompt (simple extraction)
            # In demo mode, just do basic simplification
            return None  # Will trigger demo output in convert()
        
        try:
            payload = {
                "inputs": prompt,
                "parameters": config.GENERATION_CONFIG
            }
            
            response = requests.post(
                config.API_URL,
                headers=self.headers,
                json=payload,
                timeout=config.API_TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract only the simplified version
                    if "Simplified version:" in generated_text:
                        simplified = generated_text.split("Simplified version:")[-1].strip()
                        return simplified
                    return generated_text
            else:
                print(f"⚠️  API Error {response.status_code}: {response.text}")
                return None
                
        except Exception as e:
            print(f"⚠️  API call failed: {str(e)}")
            return None
    
    def convert(self, item: AssessmentItem) -> ConversionResult:
        """
        Convert assessment item to simplified text with validation
        Works in both FULL mode (with API key) and DEMO mode (without API key)
        """
        
        original_text = item.text
        original_difficulty = self.difficulty_scorer.calculate_difficulty(original_text)
        
        for attempt in range(1, config.MAX_REGENERATION_ATTEMPTS + 1):
            
            # Generate simplified text
            if self.demo_mode:
                simplified_text = self._generate_demo_output(original_text)
                time.sleep(0.5)  # Simulate API delay
            else:
                prompt = get_simplification_prompt(original_text)
                simplified_text = self._call_llm_api(prompt)
                
                if not simplified_text:
                    # Fallback to demo mode if API fails
                    print(f"   Attempt {attempt}: API failed, using demo output")
                    simplified_text = self._generate_demo_output(original_text)
            
            # Validate semantic similarity
            semantic_score = self.semantic_checker.check_similarity(
                original_text, 
                simplified_text
            )
            
            # Calculate difficulty
            simplified_difficulty = self.difficulty_scorer.calculate_difficulty(simplified_text)
            difficulty_change = ((simplified_difficulty - original_difficulty) / original_difficulty) * 100
            
            # Check if validation passes
            semantic_pass = semantic_score >= config.SEMANTIC_SIMILARITY_THRESHOLD
            difficulty_pass = abs(difficulty_change) <= config.MAX_DIFFICULTY_CHANGE_PERCENT
            
            if semantic_pass and difficulty_pass:
                return ConversionResult(
                    id=item.id,
                    original_text=original_text,
                    simplified_text=simplified_text,
                    semantic_score=semantic_score,
                    difficulty_change=difficulty_change,
                    status="success",
                    attempts=attempt,
                    issues=[]
                )
            
            # If not last attempt, continue loop
            if attempt < config.MAX_REGENERATION_ATTEMPTS:
                issues = []
                if not semantic_pass:
                    issues.append(f"Semantic score {semantic_score:.3f} < {config.SEMANTIC_SIMILARITY_THRESHOLD}")
                if not difficulty_pass:
                    issues.append(f"Difficulty change {abs(difficulty_change):.1f}% > {config.MAX_DIFFICULTY_CHANGE_PERCENT}%")
                
                print(f"   Attempt {attempt} failed: {', '.join(issues)}")
                print(f"   Retrying...")
        
        # All attempts exhausted
        final_issues = []
        if semantic_score < config.SEMANTIC_SIMILARITY_THRESHOLD:
            final_issues.append(f"Low semantic similarity: {semantic_score:.3f}")
        if abs(difficulty_change) > config.MAX_DIFFICULTY_CHANGE_PERCENT:
            final_issues.append(f"Difficulty change too high: {abs(difficulty_change):.1f}%")
        
        return ConversionResult(
            id=item.id,
            original_text=original_text,
            simplified_text=simplified_text,
            semantic_score=semantic_score,
            difficulty_change=difficulty_change,
            status="failed",
            attempts=config.MAX_REGENERATION_ATTEMPTS,
            issues=final_issues
        )
