
from text_simplifier import TextSimplifier

def debug_issue():
    print("Initializing Simplifier...")
    simplifier = TextSimplifier()
    
    input_text = "calculate the area of the circle with radius = 6cm"
    print(f"\nProcessing: '{input_text}'")
    
    result = simplifier.simplify(input_text)
    
    print("\nFINAL RESULT:")
    print(f"Simplified: {result.get('simplified_text', 'N/A')}")
    print(f"Full Result Keys: {list(result.keys())}")
    print(f"Passed: {result.get('passed_internal_validation')}")

if __name__ == "__main__":
    try:
        debug_issue()
    except Exception as e:
        import traceback
        traceback.print_exc()
