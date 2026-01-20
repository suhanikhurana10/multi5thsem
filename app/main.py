from fastapi import FastAPI
from app.text_input_handler import router as text_router


app = FastAPI(title="Manual Text to Braille Converter")
=======
from app.text_simplifier.text_simplifier import simplify_text
from app.text_simplifier.semantic_checker import semantic_score
from app.text_simplifier.difficulty_scorer import difficulty_score

app = FastAPI(title="Braille Converter API")


app.include_router(text_router)

@app.get("/")

def root():
    return {"message": "Server running"}
=======
def home():
    return {"status": "Braille Converter API is running"}

@app.route("/simplify", methods=["POST"])
def simplify():
    data = request.get_json()
    text = data["text"]

    simplified = simplify_text(text)
    sem = semantic_score(text, simplified)
    diff = difficulty_score(simplified)

    return jsonify({
        "simplified": simplified,
        "semantic_score": sem,
        "difficulty_score": diff
    })

