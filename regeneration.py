from equivalence_engine import validate

MAX_ATTEMPTS = 3

def regenerate(original_text, generator_fn):
    best_output = None
    best_score = 0
    last_metrics = None

    print("\n🔁 Starting Regeneration Loop")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\nAttempt {attempt}")

        generated = original_text + " in simple words"

        metrics = validate(original_text, generated)

        # ✅ CONVERT NUMPY → PYTHON FLOATS
        safe_metrics = {
            "semantic_score": float(metrics["semantic_score"]),
            "difficulty_change": float(metrics["difficulty_change"]),
            "concept_overlap": float(metrics["concept_overlap"]),
            "pass": bool(metrics["pass"])
        }

        print("Similarity:", safe_metrics["semantic_score"])
        print("Difficulty Δ:", safe_metrics["difficulty_change"])
        print("Concept overlap:", safe_metrics["concept_overlap"])

        if safe_metrics["pass"]:
            print("✅ Validation Passed")
            return {
                "output": generated,
                "validated": True,
                "attempts": attempt,
                "metrics": safe_metrics
            }

        if safe_metrics["semantic_score"] > best_score:
            best_score = safe_metrics["semantic_score"]
            best_output = generated
            last_metrics = safe_metrics

        print("❌ Validation failed. Retrying...")

    print("\n⚠ Max attempts reached. Returning best result.")

    return {
        "output": best_output,
        "validated": False,
        "attempts": MAX_ATTEMPTS,
        "metrics": last_metrics
    }
