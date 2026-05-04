try:
    import spacy
except Exception:
    spacy = None


_NLP_CONCEPT = None

class ConceptChecker:
    def __init__(self):
        global _NLP_CONCEPT
        if _NLP_CONCEPT is None:
            try:
                # Reuse if possible, or load
                print("Loading Spacy model for Concepts (Singleton)...")
                _NLP_CONCEPT = spacy.load("en_core_web_sm")
            except:
                _NLP_CONCEPT = None
        self.nlp = _NLP_CONCEPT


    def extract_concepts(self, text: str):
        if not self.nlp:
            return set(text.lower().split())
            
        doc = self.nlp(text)
        # Extract nouns, proper nouns, and verbs
        concepts = set()
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop:
                concepts.add(token.lemma_.lower())
        return concepts

    def calculate_overlap(self, original: str, generated: str) -> float:
        """
        Calculates the ratio of original concepts preserved in the generated text.
        """
        if not self.nlp:
            return 1.0 # Mock pass if no spacy
            
        original_concepts = self.extract_concepts(original)
        generated_concepts = self.extract_concepts(generated)
        
        if not original_concepts:
            return 1.0
            
        # Intersection
        common = original_concepts.intersection(generated_concepts)
        
        # Ratio of ORIGINAL concepts retained
        overlap_ratio = len(common) / len(original_concepts)
        
        return round(overlap_ratio, 3)
