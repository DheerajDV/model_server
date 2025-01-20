from typing import List, Dict
import numpy as np
from collections import Counter
import re

class TextClassifier:
    def __init__(self):
        print("Initializing stock market sentiment classifier...")
        # Define stock market sentiment keywords
        self.sentiment_words = {
            'bullish': {'surge', 'rally', 'breakout', 'upgrade', 'outperform', 'buy', 'strong', 'growth',
                       'profit', 'upside', 'gain', 'positive', 'rise', 'higher', 'momentum', 'beat',
                       'exceed', 'improve', 'recovery', 'opportunity'},
            'bearish': {'decline', 'downgrade', 'sell', 'underperform', 'weak', 'loss', 'downside',
                       'fall', 'lower', 'drop', 'crash', 'risk', 'concern', 'warning', 'miss',
                       'below', 'pressure', 'volatile', 'caution', 'debt'},
            'neutral': {'hold', 'stable', 'steady', 'flat', 'unchanged', 'mixed', 'balanced',
                       'maintain', 'inline', 'expected', 'moderate', 'consolidate', 'range-bound',
                       'fair', 'normal'}
        }
        
    def _preprocess(self, text: str) -> List[str]:
        """Basic text preprocessing"""
        # Convert to lowercase and split into words
        words = text.lower().split()
        # Remove punctuation
        words = [re.sub(r'[^\w\s]', '', word) for word in words]
        # Remove empty strings
        return [word for word in words if word]
        
    def _calculate_sentiment_score(self, words: List[str], sentiment: str) -> float:
        """Calculate sentiment score based on keyword matches"""
        sentiment_words = self.sentiment_words.get(sentiment, set())
        matches = sum(1 for word in words if word in sentiment_words)
        return matches + 0.1  # Add small constant to avoid zero probabilities
        
    def predict_proba(self, text: str, labels: List[str]) -> Dict[str, float]:
        """
        Predict probability scores for each label using sentiment analysis
        """
        words = self._preprocess(text)
        
        # Calculate sentiment scores
        scores = []
        for label in labels:
            # If label is in our sentiment dictionary, use sentiment scoring
            if label.lower() in self.sentiment_words:
                score = self._calculate_sentiment_score(words, label.lower())
            else:
                # For unknown labels, use a small constant
                score = 0.1
            scores.append(score)
            
        # Convert to probabilities using softmax
        exp_scores = np.exp(scores)
        probabilities = exp_scores / exp_scores.sum()
        
        return {label: float(prob) for label, prob in zip(labels, probabilities)}
