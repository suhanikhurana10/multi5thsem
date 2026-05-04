"""
Standalone Test for Text Simplifier
Run this directly without needing backend server
Usage: python test_simplifier_module.py
"""

import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from text_simplifier import TextSimplifier
from models import AssessmentItem

def test_sample_questions():
    """Test text simplifier with sample assessment questions"""
    
    print("=" * 60)
    print("TEXT SIMPLIFIER - STANDALONE TEST")
    print("=" * 60)
    
    # Initialize simplifier
    print("\n[1/4] Initializing Text Simplifier...")
    simplifier = TextSimplifier()
    print("✓ Text Simplifier initialized successfully")
    
    # Sample test questions
    test_questions = [
        {
            "id": "Q1",
            "text": "Evaluate the definite integral of f(x) = x^2 from x = 0 to x = 5."
        },
        {
            "id": "Q2", 
            "text": "The perimeter of a rectangular garden is 48 meters. If the length is twice the width, determine the dimensions of the garden."
        },
        {
            "id": "Q3",
            "text": "Analyze the relationship between photosynthesis and cellular respiration in plants."
        }
    ]
    
    print(f"\n[2/4] Testing with {len(test_questions)} sample questions...\n")
    
    results = []
    
    for idx, question in enumerate(test_questions, 1):
        print(f"\n{'─' * 60}")
        print(f"Question {idx}/{len(test_questions)}: {question['id']}")
        print(f"{'─' * 60}")
        
        # Create assessment item
        item = AssessmentItem(
            id=question['id'],
            text=question['text']
        )
        
        print(f"\n📝 ORIGINAL TEXT:")
        print(f"   {item.text}")
        
        # Convert
        print(f"\n⚙️  Processing...")
        result = simplifier.convert(item)
        
        # Display results
        print(f"\n✨ SIMPLIFIED TEXT:")
        print(f"   {result.converted_content}")
        
        print(f"\n📊 VALIDATION SCORES:")
        print(f"   • Semantic Similarity: {result.metrics.semantic_score:.3f}")
        print(f"   • Difficulty Change: {abs(result.metrics.difficulty_change):.1f}%")
        print(f"   • Status: {result.status.value}")
        print(f"   • Attempts: {result.attempts}")
        
        if result.status.value != "passed":
            print(f"\n⚠️  STATUS NOT PASSED. Needs Review!")
        
        results.append(result)
    
    # Summary
    print(f"\n\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    
    success_count = sum(1 for r in results if r.status.value == "passed")
    print(f"\n✓ Successful conversions: {success_count}/{len(results)}")
    
    avg_semantic = sum(r.metrics.semantic_score for r in results) / len(results)
    print(f"✓ Average semantic similarity: {avg_semantic:.3f}")
    
    avg_difficulty = sum(abs(r.metrics.difficulty_change) for r in results) / len(results)
    print(f"✓ Average difficulty change: {avg_difficulty:.1f}%")
    
    print(f"\n{'=' * 60}")
    print("✓ Test completed successfully!")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    try:
        # Run sample tests
        test_sample_questions()
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nMake sure you have:")
        print("1. Installed requirements: pip install -r requirements.txt")
        print("2. Set HUGGINGFACE_API_KEY in .env file")
        import traceback
        traceback.print_exc()
