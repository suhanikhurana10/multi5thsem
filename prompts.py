"""
Prompt Engineering for Controlled Text Simplification
Ensures simplification preserves assessment validity
"""

def get_simplification_prompt(
    text: str,
    level: str = "moderate",
    preserve_math: bool = True
) -> str:
    """
    Generate prompt for Llama 3.2 to simplify assessment text.
    
    Args:
        text: Original assessment question
        level: "minimal", "moderate", or "significant" simplification
        preserve_math: Whether to preserve mathematical notation exactly
        
    Returns:
        Formatted prompt string
    """
    
    # Math preservation instruction
    math_instruction = ""
    if preserve_math:
        math_instruction = """
CRITICAL: Preserve ALL mathematical notation EXACTLY:
- Keep formulas, equations, symbols (∫, ∑, π, etc.)
- Keep numerical values and units
- Keep answer choices (A, B, C, D) unchanged"""
    
    # Simplification level guidance
    level_guidance = {
        "minimal": "Make only minor word substitutions. Keep sentence structure.",
        "moderate": "Use simpler words and shorter sentences. Break complex sentences.",
        "significant": "Use very basic vocabulary. Use very short, simple sentences."
    }
    
    prompt = f"""You are an expert at simplifying educational assessments for students with reading difficulties.

Your task: Simplify the language while testing THE SAME knowledge at THE SAME difficulty level.

RULES:
1. Test the SAME concepts and knowledge
2. Maintain the SAME cognitive challenge level
3. Only simplify the LANGUAGE, not the content difficulty
4. Preserve all key technical terms and concepts
{math_instruction}

SIMPLIFICATION LEVEL: {level_guidance.get(level, level_guidance['moderate'])}

ORIGINAL QUESTION:
{text}

SIMPLIFIED QUESTION (provide only the simplified text, no explanations):"""
    
    return prompt


def get_regeneration_prompt(
    text: str,
    failed_metric: str,
    current_simplified: str,
    level: str = "moderate"
) -> str:
    """
    Generate adjusted prompt for regeneration after validation failure.
    
    Args:
        text: Original text
        failed_metric: Which validation failed ("semantic", "difficulty", or "both")
        current_simplified: The simplified version that failed
        level: Simplification level
        
    Returns:
        Adjusted prompt with specific guidance
    """
    
    adjustment = ""
    
    if failed_metric == "semantic":
        adjustment = """
IMPORTANT ADJUSTMENT: The previous simplification changed the meaning too much.
- Stay much closer to the original wording
- Preserve all key concepts and examples
- Only change the most difficult words"""
    
    elif failed_metric == "difficulty":
        adjustment = """
IMPORTANT ADJUSTMENT: The previous simplification changed the difficulty level.
- Maintain more of the original vocabulary complexity
- Keep sentence structures that preserve cognitive challenge
- Simplify carefully to avoid making it too easy OR too hard"""
    
    elif failed_metric == "both":
        adjustment = """
IMPORTANT ADJUSTMENT: Previous attempt failed on both meaning AND difficulty.
- Make minimal changes - only substitute the hardest words
- Preserve sentence structure and all concepts
- Be very conservative in your simplification"""
    
    prompt = f"""You are simplifying an assessment question. A previous attempt failed validation.

ORIGINAL QUESTION:
{text}

PREVIOUS SIMPLIFIED VERSION (which failed):
{current_simplified}

{adjustment}

Provide a NEW simplified version that addresses these issues:"""
    
    return prompt
