print("Loading app.py...")
from flask import Flask, request, jsonify, send_from_directory

from nlp_engine import text_to_image
from regeneration import regenerate
import os

app = Flask(__name__)

# Manual CORS support
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/")
def home():
    return send_from_directory(".", "el.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "online", "message": "Server is running"}), 200

@app.route("/generate", methods=["POST"])
def generate():


    data = request.json
    question = data.get("question", "")
    mode = data.get("mode", "visual")
    
    print(f"DEBUG: Processing question: {question}")

    if not question:


        return jsonify({"error": "No question provided"}), 400

    # ---------------- VISUAL MODE ----------------
    if mode == "visual":
        output_path = text_to_image(question)

        if not output_path:
            return jsonify({
                "status": "error",
                "message": "Visual could not be generated"
            })

        return jsonify({
            "status": "success",
            "image": f"/generated_images/{os.path.basename(output_path)}"
        })

    # ---------------- TEXT MODES ----------------
    from regeneration import regenerate

    def generator_fn(q):
        return q  # or your simplifier later

    result = regenerate(question, generator_fn)

    return jsonify({
        "status": "success",
        "output": result["output"],
        "validated": result["validated"],
        "attempts": result["attempts"],
        "metrics": result["metrics"]
    })

from regeneration import regenerate

@app.route("/validate", methods=["POST"])
def validate_route():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    def dummy_generator(x):
        # For now just return simplified text
        return x + " in simple words"

    result = regenerate(text, dummy_generator)

    return jsonify({
        "validated": result["validated"],
        "attempts": result["attempts"],
        "metrics": {
            "semantic_score": float(result["metrics"]["semantic_score"]),
            "difficulty_change": float(result["metrics"]["difficulty_change"]),
            "concept_overlap": float(result["metrics"]["concept_overlap"]),
            "pass": result["metrics"]["pass"]
        }
    })


@app.route("/generated_images/<filename>")
def serve_image(filename):
    return send_from_directory("generated_images", filename)


# ---------------- PRE-LOAD MODELS ----------------
try:
    print("Initializing Text Simplifier (Pre-loading models)...")
    from text_simplifier import TextSimplifier
    _GLOBAL_SIMPLIFIER = TextSimplifier()
    print("Text Simplifier ready.")
except Exception as e:
    print(f"FAILED to load Text Simplifier: {e}")
    _GLOBAL_SIMPLifier = None

@app.route("/simplify", methods=["POST"])
def simplify_route():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    # ---------------- NEW ARCHITECTURE ----------------
    try:
        if _GLOBAL_SIMPLIFIER is None:
             raise Exception("Text Simplifier failed to initialize on startup.")
             
        result = _GLOBAL_SIMPLIFIER.simplify(text)
        
        return jsonify({
            "status": "success",
            "simplified": result["simplified_text"],
            "semantic_score": result["semantic_score"],
            "difficulty_score": result["difficulty_change"],
            "metrics": {
                "semantic_score": result["semantic_score"],
                "difficulty_change": result["difficulty_change"],
                "passed": result["passed_internal_validation"],
                "attempts": result["attempt"]
            },
            "quality_report": {
                 "status": "passed" if result["passed_internal_validation"] else "failed",
                 "needs_regeneration": result.get("needs_regeneration", False)
            },
            "is_validated": result["passed_internal_validation"]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500





@app.route("/braille", methods=["POST"])
def braille_route():
    data = request.json
    text = data.get("text", "") 
    if not text:
        return jsonify({"error": "No text provided"}), 400

    from braille_converter import to_braille
    braille_text = to_braille(text)


    return jsonify({
        "status": "success",
        "braille": braille_text,
        "original": text
    })

if __name__ == "__main__":
    print("Starting Flask Server...")
    # Threaded=True to handle multiple requests (e.g. braille + visual + simplify)
    # Host=0.0.0.0 to bind all interfaces
    app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)



