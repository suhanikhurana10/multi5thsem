from fastapi import FastAPI
from app.text_input_handler import router as text_router

app = FastAPI(title="Manual Text to Braille Converter")

app.include_router(text_router)

@app.get("/")
def root():
    return {"message": "Server running"}
