
from text_simplifier import TextSimplifier
from models import AssessmentItem

def test_simplifier():
    print("================================================================================")
    print("🧪 TEST: Text Simplifier Module Verification")
    print("================================================================================")

    # Initialize
    print("\n1. Initializing Simplifier...")
    simplifier = TextSimplifier()
    print("   ✓ Initialized")

    # Test Case 1: Math Preservation
    text_math = "Calculate the derivative of f(x) = 3x^2 + 5x - 2 using the power rule."
    print(f"\n2. Testing Math Preservation:\n   Input: '{text_math}'")
    
    result = simplifier.simplify(text_math, preserve_math=True)
    print(f"   Output: '{result['simplified_text']}'")
    
    if "f(x) = 3x^2 + 5x - 2" in result['simplified_text']:
        print("   ✅ SUCCESS: Math formula preserved exactly.")
    else:
        print("   ❌ FAILED: Math formula mangled.")

    # Test Case 2: Science Terms & Definitions (Universal Engine)
    text_bio = "The mitochondria facilitates respiration."
    print(f"\n3. Testing Science Terms:\n   Input: '{text_bio}'")
    result_bio = simplifier.simplify(text_bio)
    print(f"   Output: '{result_bio['simplified_text']}'")
    
    if "energy maker" in result_bio['simplified_text']:
         print("   ✅ SUCCESS: Biology term replaced.")
    else:
         print("   ❌ FAILED: Biology term not replaced.")

    # Test Case 3: Standardized Interface
    print("\n4. Testing Standardized Interface (AssessmentItem)...")
    item = AssessmentItem(
        id="Q001",
        text="It is important to note that the velocity increased.",
        has_math=False
    )
    
    conversion = simplifier.convert(item)
    print(f"   Status: {conversion.status.value}")
    print(f"   Converted: '{conversion.converted_content}'")
    print(f"   Metrics: {conversion.metrics.to_dict()}")

    if conversion.status.value == "passed":
        print("   ✅ SUCCESS: Interface returned valid result.")
    else:
        print("   ⚠️ NOTE: Interface returned needs_review (check metrics).")

if __name__ == "__main__":
    test_simplifier()
