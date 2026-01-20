from sentence_transformers import SentenceTransformer, util
import textstat
import spacy

# Load models once
model = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

SIMILARITY_THRESHOLD = 0.85
MAX_DIFFICULTY_CHANGE = 10
MIN_CONCEPT_OVERLAP = 0.6


# ------------------ CORE METRICS ------------------

def semantic_similarity(text1, text2):
    if not text1 or not text2:
        return 0.0

    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    score = float(util.cos_sim(emb1, emb2))
    return round(score, 4)


def difficulty_score(text):
    try:
        return textstat.flesch_reading_ease(text)
    except:
        return 0


def concept_overlap(text1, text2):
    doc1 = nlp(text1)
    doc2 = nlp(text2)

    key1 = {t.lemma_ for t in doc1 if t.pos_ in ["NOUN", "VERB"]}
    key2 = {t.lemma_ for t in doc2 if t.pos_ in ["NOUN", "VERB"]}

    if not key1:
        return 0.0

    return round(len(key1 & key2) / len(key1), 3)


# ------------------ MAIN VALIDATION ------------------

def validate(original, generated):
    sim = float(semantic_similarity(original, generated))
    diff = float(abs(difficulty_score(original) - difficulty_score(generated)))
    concept = float(concept_overlap(original, generated))

    return {
        "semantic_score": sim,
        "difficulty_change": diff,
        "concept_overlap": concept,
        "pass": (
            sim >= SIMILARITY_THRESHOLD and
            diff <= MAX_DIFFICULTY_CHANGE and
            concept >= 0.6
        )
    }


    print("\n--- EQUIVALENCE CHECK ---")
    print("Similarity:", sim)
    print("Difficulty Δ:", diff)
    print("Concept overlap:", concept)
    print("Pass:", passed)

    return {
        "semantic_score": sim,
        "difficulty_change": diff,
        "concept_overlap": concept,
        "pass": passed
    }
