# Text Simplification Module

**Part of the Adaptive Multi-Format Assessment Generator**  
**SDG 4: Quality Education - V Semester EL Project**

Automated text simplification for assessment questions with semantic equivalence validation and difficulty alignment.

---

## 🎯 Features

- **Semantic Similarity Validation**: Ensures simplified text maintains meaning (>0.85 threshold using Sentence-BERT)
- **Difficulty Preservation**: Keeps cognitive difficulty aligned (<10% change using multi-factor scoring)
- **Math Notation Preservation**: Maintains exact mathematical expressions and formulas
- **Adaptive Regeneration**: Automatically retries with adjusted parameters (up to 3 attempts)
- **Automatic Flagging**: Flags items that fail validation for manual review
- **Production-Ready**: Comprehensive logging, error handling, and standardized interfaces

---

## 📦 Installation

### 1. Clone Repository
```bash
git clone https://github.com/suhanikhurana10/5thsemel.git
cd 5thsemel
git checkout text-simplifier
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 4. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Hugging Face token
# Get your token from: https://huggingface.co/settings/tokens
```

Your `.env` file should look like:
```
HF_TOKEN=hf_your_actual_token_here
SEMANTIC_THRESHOLD=0.85
DIFFICULTY_THRESHOLD=10.0
MAX_ATTEMPTS=3
```

---

## 🚀 Usage

### Basic Usage (Standalone)

```python
from text_simplifier import TextSimplifier

# Initialize with your Hugging Face token
simplifier = TextSimplifier()  # Reads token from .env

# Simplify a question
result = simplifier.simplify(
    original_text="Calculate the derivative of f(x) = 3x² + 5x - 2 using the power rule.",
    simplification_level="moderate",
    preserve_math=True
)

print(result['simplified_text'])
print(f"✓ Success: {result['success']}")
print(f"📊 Semantic score: {result['semantic_score']:.3f}")
print(f"📊 Difficulty change: {result['difficulty_change']:.1f}%")
```

### Team Integration (Standardized Interface)

```python
from text_simplifier import TextSimplifier
from models import AssessmentItem

# Initialize
simplifier = TextSimplifier()

# Create assessment item
item = AssessmentItem(
    id="Q001",
    text="Calculate the derivative of f(x) = 3x² + 5x - 2",
    has_math=True,
    difficulty_level="medium"
)

# Convert using standardized interface
result = simplifier.convert(
    item=item,
    simplification_level="moderate",
    preserve_math=True
)

# Access standardized fields
print(f"Status: {result.status.value}")
print(f"Validated: {result.is_validated}")
print(f"Needs Review: {result.needs_review}")
print(f"Simplified: {result.converted_content}")
print(f"Metrics: {result.metrics.to_dict()}")
```

---

## 📊 Validation Metrics

| Metric | Threshold | Method |
|--------|-----------|--------|
| **Semantic Similarity** | > 0.85 | Sentence-BERT (all-MiniLM-L6-v2) |
| **Difficulty Change** | < 10% | Composite score (Flesch-Kincaid + lexical analysis) |
| **Math Preservation** | 100% | Exact notation matching |

### Difficulty Scoring Components
- Flesch Reading Ease (30% weight)
- Flesch-Kincaid Grade Level (30% weight)
- Average Word Length (20% weight)
- Average Sentence Length (20% weight)

---

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

```bash
# Required
HF_TOKEN=your_token_here

# Validation Thresholds
SEMANTIC_THRESHOLD=0.85        # Minimum semantic similarity (0-1)
DIFFICULTY_THRESHOLD=10.0      # Maximum difficulty change percentage
MAX_ATTEMPTS=3                 # Maximum regeneration attempts

# Model Configuration
LLM_MODEL=meta-llama/Llama-3.2-3B-Instruct
EMBEDDING_MODEL=all-MiniLM-L6-v2
SPACY_MODEL=en_core_web_sm

# Generation Parameters
BASE_TEMPERATURE=0.3           # Starting temperature for LLM
TEMPERATURE_INCREMENT=0.15     # Temperature increase per retry
MAX_TOKENS=300                 # Maximum tokens in response
```

---

## 📁 Project Structure

```
text-simplifier/
├── text_simplifier.py      # Main simplification engine
├── semantic_checker.py     # Semantic similarity validation
├── difficulty_scorer.py    # Text difficulty analysis
├── prompts.py             # LLM prompt templates
├── models.py              # Standardized data models (for team integration)
├── config.py              # Configuration management
├── example.py             # Usage examples
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

---

## 🔄 Adaptive Regeneration Flow

```
┌─────────────────────────┐
│  Input Question         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Generate Simplified    │◄──┐
│  (Temperature: 0.3+)    │   │
└───────────┬─────────────┘   │
            │                 │
            ▼                 │
┌─────────────────────────┐   │
│  Validate:              │   │
│  • Semantic > 0.85      │   │
│  • Difficulty < 10%     │   │
└───────────┬─────────────┘   │
            │                 │
      ┌─────┴─────┐           │
      │           │           │
   PASS        FAIL           │
      │           │           │
      ▼           ▼           │
   ✅ Done    ⚠️ Retry ───────┘
              (Max 3 attempts)
              │
              ▼
          🚩 Flag for Manual Review
```

---

## 🤝 Integration with Team Modules

This module is designed to integrate seamlessly with:

- **Text-to-Audio** (Arshia): Takes simplified text as input
- **Text-to-Braille** (Vinith): Converts simplified text to braille format
- **Text-to-Visual** (Suhani): Uses simplified text for image generation

### Standardized Interface

All modules follow the same pattern:

```python
def convert(item: AssessmentItem, **kwargs) -> ConversionResult:
    """
    Convert assessment item to target format.
    
    Args:
        item: Standardized assessment item
        **kwargs: Format-specific parameters
        
    Returns:
        ConversionResult with validation metrics
    """
```

---

## 🧪 Testing

Run the example script to test the module:

```bash
python example.py
```

Expected output:
```
================================================================================
SIMPLIFYING: Calculate the derivative of the function f(x) = 3x² + 5x - 2...
================================================================================

🔄 Attempt 1/3
  📊 Semantic: 0.894 ✓
  📊 Difficulty: 4.2% change ✓
  ✅ All checks passed!

ORIGINAL: Calculate the derivative of the function f(x) = 3x² + 5x - 2 using the power rule.
SIMPLIFIED: Find the derivative of f(x) = 3x² + 5x - 2 using the power rule.
STATUS: ✅ PASSED
Semantic: 0.894 | Difficulty Change: 4.2%
```

---

## 🐛 Troubleshooting

### "HF_TOKEN is required" Error
- Make sure you've created a `.env` file (copy from `.env.example`)
- Add your Hugging Face token to the `.env` file
- Get token from: https://huggingface.co/settings/tokens

### "spacy model not found" Error
```bash
python -m spacy download en_core_web_sm
```

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

---

## 📝 Development Notes

### For Team Members
- Always use the `convert()` method for new integrations (returns `ConversionResult`)
- The legacy `simplify()` method is kept for backward compatibility
- All validation thresholds are configurable via `.env`
- Check `result.is_validated` before using output in production

### Performance
- First run loads models (~2-3 seconds)
- Subsequent simplifications: ~1-2 seconds per item
- Batch processing recommended for multiple items

---

## 📚 References

1. Sentence-BERT: [https://www.sbert.net/](https://www.sbert.net/)
2. Meta Llama 3.2: [https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)
3. Textstat Documentation: [https://pypi.org/project/textstat/](https://pypi.org/project/textstat/)

---

## 👥 Team

- **Aditi Rajesh** - Text Simplification Module
- **Arshia Sirohi** - Team Lead, Text-to-Audio
- **Suhani Khurana** - Text-to-Image
- **Vinith** - Text-to-Braille

**Course**: V Semester B.E Programs - Experiential Learning for SDG 4  
**Institution**: R.V. College of Engineering  
**Academic Year**: 2025-26

---

## 📄 License

MIT License - See project repository for details
