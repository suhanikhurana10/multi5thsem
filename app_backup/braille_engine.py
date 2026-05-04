import os
import uuid

BRAILLE_MAP = {
    "a": "⠁", "b": "⠃", "c": "⠉", "d": "⠙",
    "e": "⠑", "f": "⠋", "g": "⠛", "h": "⠓",
    "i": "⠊", "j": "⠚", "k": "⠅", "l": "⠇",
    "m": "⠍", "n": "⠝", "o": "⠕", "p": "⠏",
    "q": "⠟", "r": "⠗", "s": "⠎", "t": "⠞",
    "u": "⠥", "v": "⠧", "w": "⠺", "x": "⠭",
    "y": "⠽", "z": "⠵", " ": " "
}

def convert_to_braille(text: str) -> str:
    os.makedirs("outputs", exist_ok=True)

    braille_text = ""
    for ch in text.lower():
        braille_text += BRAILLE_MAP.get(ch, ch)

    filename = f"outputs/braille_{uuid.uuid4().hex}.brf"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(braille_text)

    return filename
