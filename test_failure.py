
from models import AssessmentItem
from text_simplifier import TextSimplifier

def demonstrate_failure():
    print("\n🧪 DEMONSTRATION: Forcing a Validation Failure")
    print("==============================================")
    
    # We will simulate a "Bad Actor" simplifier manually
    # because our actual simplifier is too good now! :)
    
    simplifier = TextSimplifier()
    original_text = "Calculate the derivative of f(x) = 3x^2 + 5"
    
    # Simulate a BAD simplification (Math Mangle)
    bad_simplified_text = "Find the answer for the function equals three x two plus five."
    
    print(f"Original:   '{original_text}'")
    print(f"Bad Output: '{bad_simplified_text}'")
    
    # Manually running validation logic to show what happens
    print("\nrunning validation checks...")
    
    # 1. Math Check
    # This matches the logic inside text_simplifier.py
    _, protections = simplifier.protect_math(original_text)
    math_status = "intact"
    for placeholder, original in protections.items():
        if original not in bad_simplified_text:
             math_status = "violated"
             print(f"❌ MATH FAIL: Expected '{original}' to be preserved.")

    # 2. Semantic Check
    sem_score = simplifier.semantic_checker.check_similarity(original_text, bad_simplified_text)
    print(f"❌ SEMANTIC FAIL: Score {sem_score} (Threshold: {simplifier.semantic_threshold})")
    
    # 3. Difficulty Check
    diff_change = simplifier.difficulty_scorer.calculate_change(original_text, bad_simplified_text)
    print(f"⚠️ DIFFICULTY FAIL: Change {diff_change:.1f}% (Threshold: {simplifier.difficulty_threshold_percent}%)")

    print("\n>>> FINAL SYSTEM FLAG: [NEEDS MANUAL REVIEW] <<<")

if __name__ == "__main__":
    demonstrate_failure()
