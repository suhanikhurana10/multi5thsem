"""
Configuration management for the text simplifier.
"""
import os
from typing import Optional

class Config:
    """Configuration settings for the text simplification module."""
    
    def __init__(self):
        # Hugging Face API token
        self.HF_TOKEN: Optional[str] = os.getenv("HF_TOKEN")
        
        # Validation thresholds
        self.SEMANTIC_THRESHOLD: float = float(os.getenv("SEMANTIC_THRESHOLD", "0.85"))
        self.DIFFICULTY_THRESHOLD: float = float(os.getenv("DIFFICULTY_THRESHOLD", "10.0"))
        self.MAX_ATTEMPTS: int = int(os.getenv("MAX_ATTEMPTS", "3"))
        
        # Model configuration
        self.LLM_MODEL: str = os.getenv("LLM_MODEL", "meta-llama/Llama-3.2-3B-Instruct")
        self.EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
        self.SPACY_MODEL: str = os.getenv("SPACY_MODEL", "en_core_web_sm")
        
        # Generation parameters
        self.BASE_TEMPERATURE: float = float(os.getenv("BASE_TEMPERATURE", "0.3"))
        self.TEMPERATURE_INCREMENT: float = float(os.getenv("TEMPERATURE_INCREMENT", "0.15"))
        self.MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "300"))
    
    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.HF_TOKEN:
            raise ValueError(
                "HF_TOKEN environment variable is required. "
                "Get your token from https://huggingface.co/settings/tokens"
            )
        return True

# Global config instance
config = Config()
