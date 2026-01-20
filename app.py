from flask import Flask, request, jsonify, send_from_directory
from nlp_engine import text_to_image
from regeneration import regenerate
import os

app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory(".", "el.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    question = data.get("question", "")
    mode = data.get("mode", "visual")

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

if __name__ == "__main__":
    app.run(debug=True)
