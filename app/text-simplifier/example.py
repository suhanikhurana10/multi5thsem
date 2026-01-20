"""
Example usage of the text simplification system.
Demonstrates both legacy interface and new standardized interface.
"""

from text_simplifier import TextSimplifier
from models import AssessmentItem
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

print("="*80)
print("TEXT SIMPLIFICATION MODULE - EXAMPLE USAGE")
print("="*80)

# Initialize simplifier (reads HF_TOKEN from .env)
try:
    simplifier = TextSimplifier()
except ValueError as e:
    print(f"\n❌ ERROR: {e}")
    print("\n📝 Quick Fix:")
    print("1. Copy .env.example to .env")
    print("2. Get your token from: https://huggingface.co/settings/tokens")
    print("3. Add it to .env file: HF_TOKEN=your_token_here")
    exit(1)

# Test questions
test_questions = [
    {
        "id": "Q001",
        "text": "Calculate the derivative of the function f(x) = 3x² + 5x - 2 using the power rule.",
        "has_math": True,
    },
    {
        "id": "Q002", 
        "text": "Determine the value of x in the equation 3x + 7 = 22 by performing inverse operations.",
        "has_math": True,
    },
    {
        "id": "Q003",
        "text": "The photosynthetic process converts light energy into chemical energy through complex biochemical reactions involving chlorophyll molecules.",
        "has_math": False,
    },
]

print("\n" + "="*80)
print("EXAMPLE 1: LEGACY INTERFACE (Backward Compatibility)")
print("="*80)

results = []
for question in test_questions[:1]:  # Just show one example
    result = simplifier.simplify(
        original_text=question["text"],
        simplification_level="moderate",
        preserve_math=question["has_math"]
    )
    results.append(result)
    
    print(f"\nORIGINAL: {question['text']}")
    print(f"SIMPLIFIED: {result['simplified_text']}")
    print(f"STATUS: {'✅ PASSED' if result['success'] else '⚠️ FLAGGED'}")
    print(f"📊 Semantic: {result['semantic_score']:.3f} | Difficulty Change: {result['difficulty_change']:.1f}%")

print("\n" + "="*80)
print("EXAMPLE 2: NEW STANDARDIZED INTERFACE (Team Integration)")
print("="*80)

conversion_results = []
for question in test_questions:
    # Create AssessmentItem
    item = AssessmentItem(
        id=question["id"],
        text=question["text"],
        has_math=question["has_math"],
        difficulty_level="medium"
    )
    
    # Use standardized convert() method
    result = simplifier.convert(
        item=item,
        simplification_level="moderate",
        preserve_math=question["has_math"]
    )
    conversion_results.append(result)
    
    print(f"\n{'='*80}")
    print(f"ITEM ID: {question['id']}")
    print(f"ORIGINAL: {question['text']}")
    print(f"SIMPLIFIED: {result.converted_content}")
    print(f"STATUS: {result.status.value.upper()}")
    print(f"✓ Validated: {result.is_validated}")
    print(f"⚠️ Needs Review: {result.needs_review}")
    print(f"🔄 Iterations: {result.iterations_taken}")
    print(f"\nMETRICS:")
    print(f"  • Semantic Similarity: {result.metrics.semantic_similarity:.3f} {'✓' if result.metrics.semantic_pass else '✗'}")
    print(f"  • Difficulty Change: {result.metrics.difficulty_change:.1f}% {'✓' if result.metrics.difficulty_pass else '✗'}")

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

# Calculate statistics
total = len(conversion_results)
validated = sum(1 for r in conversion_results if r.is_validated)
flagged = sum(1 for r in conversion_results if r.needs_review)

avg_semantic = sum(r.metrics.semantic_similarity for r in conversion_results) / total
avg_difficulty = sum(r.metrics.difficulty_change for r in conversion_results) / total
avg_iterations = sum(r.iterations_taken for r in conversion_results) / total

print(f"\n✅ VALIDATED: {validated}/{total} ({validated/total*100:.1f}%)")
print(f"⚠️  FLAGGED: {flagged}/{total} ({flagged/total*100:.1f}%)")
print(f"\n📊 Average Metrics:")
print(f"   • Semantic Similarity: {avg_semantic:.3f}")
print(f"   • Difficulty Change: {avg_difficulty:.1f}%")
print(f"   • Iterations per Item: {avg_iterations:.1f}")

print("\n" + "="*80)
print("EXPORT TO JSON (For Dashboard Integration)")
print("="*80)

# Show how to export results as JSON
import json

json_output = {
    "assessment_id": "DEMO_001",
    "total_items": total,
    "validated_items": validated,
    "flagged_items": flagged,
    "items": [result.to_dict() for result in conversion_results]
}

print(f"\n{json.dumps(json_output, indent=2)[:500]}...")
print(f"\n💾 This JSON can be sent to the dashboard or saved to a file")

print("\n" + "="*80)
print("✅ EXAMPLE COMPLETED")
print("="*80)
