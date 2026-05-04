"""
Semantic Similarity Checker using Sentence-BERT
Internal validator for text simplification module
"""

from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticChecker:
    """
    Validates that simplified text preserves original meaning.
    Uses Sentence-BERT for semantic similarity computation.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize with Sentence-BERT model.
        
        Args:
            model_name: HuggingFace model ID for sentence embeddings
        """
        print(f"Loading Sentence-BERT model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Subject: Semantic checker ready")
    
    def check_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.
        
        Args:
            text1: Original text
            text2: Simplified text
            
        Returns:
            Similarity score between 0 and 1 (higher = more similar)
        """
        # Generate embeddings
        embeddings = self.model.encode([text1, text2])
        
        # Compute cosine similarity
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        
        return float(similarity)
    
    def batch_check_similarity(self, original_texts: list, simplified_texts: list) -> list:
        """
        Check similarity for multiple text pairs at once.
        
        Args:
            original_texts: List of original texts
            simplified_texts: List of simplified texts
            
        Returns:
            List of similarity scores
        """
        if len(original_texts) != len(simplified_texts):
            raise ValueError("Lists must have same length")
        
        scores = []
        for orig, simp in zip(original_texts, simplified_texts):
            scores.append(self.check_similarity(orig, simp))
        
        return scores
