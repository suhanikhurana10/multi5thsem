class SimplificationPrompts:
    """Prompt templates for controlled text simplification."""
    
    @staticmethod
    def get_simplification_prompt(question, target_level="moderate", preserve_math=True):
        """Generate prompt for LLM to simplify while preserving validity."""
        
        math_instruction = ""
        if preserve_math:
            math_instruction = "Keep ALL math notation, formulas, and equations EXACTLY as written."
        
        difficulty_guidance = {
            "minimal": "Make only minor word substitutions.",
            "moderate": "Use simpler words and shorter sentences.",
            "significant": "Use very basic vocabulary and very short sentences."
        }
        
        prompt = f"""Simplify this assessment question for students with reading difficulties.

RULES:
- Test the SAME knowledge
- Only simplify the LANGUAGE, not the concept difficulty
{math_instruction}

LEVEL: {difficulty_guidance[target_level]}

QUESTION: {question}

Provide only the simplified question:"""
        
        return prompt
