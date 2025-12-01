import re
from typing import Dict, Tuple, List

class SentimentAdapter:
    def analyse_text(self, text: str) -> str:
        raise NotImplementedError("Implement in subclass")

class RuleBasedSentimentAdapter(SentimentAdapter):
    def __init__(self):
        # Simple keyword lists
        self.positive_words = {
            "good", "great", "excellent", "amazing", "love", "loved", "fantastic", "happy",
            "satisfied", "recommend", "nice", "pleasant", "awesome", "brilliant", "wonderful"
        }
        self.negative_words = {
            "bad", "terrible", "awful", "hate", "hated", "poor", "unhappy", "disappointed",
            "worst", "horrible", "issue", "problem", "slow", "rude", "expensive"
        }
        self.stopwords = {
            "the","a","an","and","or","but","if","then","with","without","to","from","for",
            "on","in","out","of","at","by","it","is","was","be","are","were","this","that",
            "i","you","he","she","we","they","my","your","our","their","as"
        }

    def analyse_text(self, text: str) -> str:
        tokens = self._tokenise(text)
        pos = sum(1 for t in tokens if t in self.positive_words)
        neg = sum(1 for t in tokens if t in self.negative_words)
        if pos > neg:
            return "positive"
        elif neg > pos:
            return "negative"
        else:
            return "neutral"

    def extract_keywords(self, text: str) -> List[str]:
        tokens = self._tokenise(text)
        return [t for t in tokens if t not in self.stopwords and len(t) > 2]

    def _tokenise(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z']+", text.lower())


