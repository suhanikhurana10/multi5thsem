import textstat
import spacy

class DifficultyScorer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
    
    def calculate_difficulty(self, text: str):
        """Calculate composite difficulty score (0-100, higher = harder)."""
        flesch_reading_ease = textstat.flesch_reading_ease(text)
        flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
        
        doc = self.nlp(text)
        num_words = len([token for token in doc if not token.is_punct])
        num_sentences = len(list(doc.sents))
        
        avg_word_length = sum(len(token.text) for token in doc if not token.is_punct) / max(num_words, 1)
        avg_sentence_length = num_words / max(num_sentences, 1)
        
        # Normalize metrics to 0-100 scale
        normalized_fre = max(0, min(100, (100 - flesch_reading_ease)))
        normalized_fkg = max(0, min(100, (flesch_kincaid_grade / 18) * 100))
        normalized_awl = max(0, min(100, ((avg_word_length - 3) / 5) * 100))
        normalized_asl = max(0, min(100, ((avg_sentence_length - 10) / 20) * 100))
        
        # Weighted composite score
        composite = (normalized_fre * 0.3 + normalized_fkg * 0.3 + 
                    normalized_awl * 0.2 + normalized_asl * 0.2)
        
        return {
            "composite_difficulty": round(composite, 2),
            "flesch_reading_ease": round(flesch_reading_ease, 2),
            "flesch_kincaid_grade": round(flesch_kincaid_grade, 2),
        }
