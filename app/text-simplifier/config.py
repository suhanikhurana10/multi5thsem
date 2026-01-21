"""
Configuration for Text Simplifier
Modified to work for teammates without manual setup
"""

import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# API Configuration with fallback
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', '')

# If no API key found, provide helpful message but don't crash
if not HUGGINGFACE_API_KEY:
    print("⚠️  WARNING: HUGGINGFACE_API_KEY not found in environment")
    print("   The module will work in DEMO MODE with sample outputs")
    print("   To enable full functionality:")
    print("   1. Create a .env file in this folder")
    print("   2. Add: HUGGINGFACE_API_KEY=your_key_here")
    print()

# Model Configuration
MODEL_NAME = "meta-llama/Llama-3.2-3B-Instruct"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

# Validation Thresholds
SEMANTIC_SIMILARITY_THRESHOLD = 0.85
MAX_DIFFICULTY_CHANGE_PERCENT = 10.0

# Regeneration Settings
MAX_REGENERATION_ATTEMPTS = 3

# Generation Parameters
GENERATION_CONFIG = {
    "max_new_tokens": 500,
    "temperature": 0.3,
    "top_p": 0.9,
    "do_sample": True
}

# Timeout settings (in seconds)
API_TIMEOUT = 30
