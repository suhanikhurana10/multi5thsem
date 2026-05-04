from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticChecker:
    def __init__(self):
        print("Loading Sentence-BERT model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Model loaded!")
    
    def check_similarity(self, text1, text2):
        """Calculate semantic similarity between two texts (0-1 scale)."""
        embeddings = self.model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)
