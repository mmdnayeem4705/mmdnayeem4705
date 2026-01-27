"""
Language Detection and Text Analysis Tool
Detects language from text and counts letters/words/characters
"""

import pickle
import re
import os
from typing import Dict, List, Optional


def count_characters(text: str) -> int:
    """Count total characters (excluding spaces)"""
    return len(text.replace(' ', ''))


def count_words(text: str) -> int:
    """Count words in text (handles multiple languages)"""
    words = [w for w in text.split() if w.strip()]
    return len(words)


def count_letters(text: str) -> int:
    """Count only alphabetic characters (letters) including Unicode"""
    # Matches letters from various scripts (Latin, Cyrillic, Arabic, Chinese, etc.)
    return len(re.findall(r'[a-zA-Z\u00C0-\u024F\u0370-\u1EFF\u0400-\u04FF\u0600-\u06FF\u0700-\u074F\u0750-\u077F\u0800-\u4DBF\u4E00-\u9FFF\uAC00-\uD7AF]', text))


def analyze_text(text: str) -> Dict:
    """
    Analyze text and return comprehensive statistics
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with character counts, word counts, and letter counts
    """
    return {
        'total_characters': len(text),
        'characters_no_spaces': count_characters(text),
        'words': count_words(text),
        'letters': count_letters(text),
        'spaces': text.count(' '),
        'lines': len(text.split('\n'))
    }


class LanguageDetector:
    """Language detection and text analysis class"""
    
    def __init__(self, model_path: str = 'multilingual_detector_model.pkl'):
        """
        Initialize the language detector
        
        Args:
            model_path: Path to the trained model file
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                f"Please train the model first by running: python model_trainer.py"
            )
        
        # Load model
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.model = model_data['model']
        self.reverse_label_encoder = model_data['reverse_label_encoder']
        self.labels = model_data['labels']
        
        print(f"Model loaded successfully from {model_path}")
        print(f"Supported languages: {', '.join(self.labels)}")
    
    def detect_language(self, text: str, return_probabilities: bool = False) -> Dict:
        """
        Detect the language of the input text
        
        Args:
            text: Input text to analyze
            return_probabilities: If True, return probabilities for all languages
            
        Returns:
            Dictionary with detected language and optional probabilities
        """
        if not text or not text.strip():
            return {
                'language': None,
                'confidence': 0.0,
                'message': 'Empty text provided'
            }
        
        # Vectorize text
        X_vectorized = self.vectorizer.transform([text])
        
        # Predict
        prediction_idx = self.model.predict(X_vectorized)[0]
        probabilities = self.model.predict_proba(X_vectorized)[0]
        
        predicted_language = self.reverse_label_encoder[prediction_idx]
        confidence = probabilities[prediction_idx]
        
        result = {
            'language': predicted_language,
            'confidence': float(confidence)
        }
        
        if return_probabilities:
            result['probabilities'] = {
                self.reverse_label_encoder[i]: float(prob)
                for i, prob in enumerate(probabilities)
            }
        
        return result
    
    def analyze(self, text: str, include_probabilities: bool = False) -> Dict:
        """
        Complete analysis: detect language and count statistics
        
        Args:
            text: Input text to analyze
            include_probabilities: If True, include probabilities for all languages
            
        Returns:
            Dictionary with language detection and text statistics
        """
        # Language detection
        lang_result = self.detect_language(text, return_probabilities=include_probabilities)
        
        # Text statistics
        stats = analyze_text(text)
        
        # Combine results
        result = {
            'detected_language': lang_result['language'],
            'confidence': lang_result['confidence'],
            'statistics': stats
        }
        
        if include_probabilities and 'probabilities' in lang_result:
            result['all_probabilities'] = lang_result['probabilities']
        
        return result
    
    def analyze_page(self, text: str, include_probabilities: bool = False) -> Dict:
        """
        Analyze a full page of text with detailed breakdown
        
        Args:
            text: Input text (can be multiple paragraphs/lines)
            include_probabilities: If True, include probabilities for all languages
            
        Returns:
            Comprehensive analysis including per-line breakdown
        """
        lines = text.split('\n')
        line_analyses = []
        
        for line_num, line in enumerate(lines, 1):
            if line.strip():
                line_result = self.analyze(line, include_probabilities=False)
                line_analyses.append({
                    'line_number': line_num,
                    'text': line,
                    'language': line_result['detected_language'],
                    'confidence': line_result['confidence'],
                    'letter_count': line_result['statistics']['letters'],
                    'word_count': line_result['statistics']['words'],
                    'character_count': line_result['statistics']['characters_no_spaces']
                })
        
        # Overall analysis
        overall = self.analyze(text, include_probabilities=include_probabilities)
        
        # Language distribution
        if line_analyses:
            lang_counts = {}
            for line_analysis in line_analyses:
                lang = line_analysis['language']
                lang_counts[lang] = lang_counts.get(lang, 0) + 1
            
            overall['line_breakdown'] = line_analyses
            overall['languages_present'] = list(lang_counts.keys())
            overall['language_distribution'] = lang_counts
        
        return overall


def main():
    """Example usage of the LanguageDetector"""
    import sys
    
    # Check if model exists
    model_path = 'multilingual_detector_model.pkl'
    
    if not os.path.exists(model_path):
        print("Error: Model not found!")
        print("Please train the model first by running: python model_trainer.py")
        sys.exit(1)
    
    # Initialize detector
    detector = LanguageDetector(model_path)
    
    # Example texts in different languages
    sample_texts = [
        "Hello, how are you today?",
        "Hola, ¿cómo estás hoy?",
        "Bonjour, comment allez-vous?",
        "안녕하세요, 오늘 어떻게 지내세요?",
        "你好，你今天怎么样？"
    ]
    
    print("\n" + "="*60)
    print("LANGUAGE DETECTION AND TEXT ANALYSIS")
    print("="*60)
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n--- Example {i} ---")
        print(f"Text: {text}")
        
        result = detector.analyze(text, include_probabilities=False)
        
        print(f"Detected Language: {result['detected_language']} (confidence: {result['confidence']:.4f})")
        print(f"Statistics:")
        print(f"  - Total Characters: {result['statistics']['total_characters']}")
        print(f"  - Characters (no spaces): {result['statistics']['characters_no_spaces']}")
        print(f"  - Words: {result['statistics']['words']}")
        print(f"  - Letters: {result['statistics']['letters']}")
        print(f"  - Spaces: {result['statistics']['spaces']}")
    
    # Example with multi-line text
    print("\n" + "="*60)
    print("PAGE ANALYSIS EXAMPLE")
    print("="*60)
    
    page_text = """Hello, this is English text.
Hola, esto es texto en español.
Bonjour, ceci est du texte en français."""
    
    print(f"\nPage Text:\n{page_text}\n")
    
    page_result = detector.analyze_page(page_text, include_probabilities=False)
    
    print(f"Overall Detected Language: {page_result['detected_language']}")
    print(f"Languages Present: {', '.join(page_result.get('languages_present', []))}")
    print(f"\nOverall Statistics:")
    stats = page_result['statistics']
    print(f"  - Total Letters: {stats['letters']}")
    print(f"  - Total Words: {stats['words']}")
    print(f"  - Total Characters (no spaces): {stats['characters_no_spaces']}")
    
    if 'line_breakdown' in page_result:
        print(f"\nLine-by-Line Breakdown:")
        for line_info in page_result['line_breakdown']:
            print(f"  Line {line_info['line_number']}: {line_info['language']} - "
                  f"{line_info['letter_count']} letters, {line_info['word_count']} words")


if __name__ == '__main__':
    main()
