"""
Difficulty Scoring using Flesch-Kincaid and spaCy
Internal validator for text simplification module
"""

import textstat
import spacy

class DifficultyScorer:
    """
    Measures text difficulty using multiple readability metrics.
    Ensures simplified text maintains similar cognitive challenge.
    """
    
    def __init__(self):
        """Initialize with spaCy English model"""
        print("Loading spaCy model for difficulty analysis...")
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️  spaCy model not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        print("Subject: Difficulty scorer ready")
    
    def calculate_difficulty(self, text: str) -> dict:
        """
        Calculate comprehensive difficulty score.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with:
                - composite_difficulty: 0-100 scale (higher = harder)
                - flesch_reading_ease: Standard readability score
                - flesch_kincaid_grade: Grade level
                - avg_word_length: Average characters per word
                - avg_sentence_length: Average words per sentence
        """
        # Flesch-Kincaid metrics
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        
        # spaCy linguistic analysis
        doc = self.nlp(text)
        words = [token for token in doc if not token.is_punct]
        sentences = list(doc.sents)
        
        num_words = len(words)
        num_sentences = len(sentences)
        
        avg_word_length = (
            sum(len(token.text) for token in words) / num_words 
            if num_words > 0 else 0
        )
        avg_sentence_length = num_words / num_sentences if num_sentences > 0 else 0
        
        # Normalize metrics to 0-100 scale
        # Flesch Reading Ease: 100 (easy) to 0 (hard) → invert it
        normalized_fre = max(0, min(100, (100 - flesch_reading_ease)))
        
        # Flesch-Kincaid Grade: 0-18+ → scale to 0-100
        normalized_fkg = max(0, min(100, (flesch_kincaid_grade / 18) * 100))
        
        # Average Word Length: 3-8 chars typical → scale to 0-100
        normalized_awl = max(0, min(100, ((avg_word_length - 3) / 5) * 100))
        
        # Average Sentence Length: 10-30 words typical → scale to 0-100
        normalized_asl = max(0, min(100, ((avg_sentence_length - 10) / 20) * 100))
        
        # Weighted composite score
        composite = (
            normalized_fre * 0.3 +
            normalized_fkg * 0.3 +
            normalized_awl * 0.2 +
            normalized_asl * 0.2
        )
        
        return {
            'composite_difficulty': round(composite, 2),
            'flesch_reading_ease': round(flesch_reading_ease, 2),
            'flesch_kincaid_grade': round(flesch_kincaid_grade, 2),
            'avg_word_length': round(avg_word_length, 2),
            'avg_sentence_length': round(avg_sentence_length, 2)
        }
    
    def compute_change(self, original: str, simplified: str) -> float:
        """
        Compute percentage change in difficulty between texts.
        
        Args:
            original: Original text
            simplified: Simplified text
            
        Returns:
            Percentage change (negative = easier, positive = harder)
        """
        orig_diff = self.calculate_difficulty(original)
        simp_diff = self.calculate_difficulty(simplified)
        
        orig_score = orig_diff['composite_difficulty']
        simp_score = simp_diff['composite_difficulty']
        
        if orig_score == 0:
            return 0
        
        return ((simp_score - orig_score) / orig_score) * 100
