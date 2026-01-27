"""
Model Training Script for Multilingual Language Detection
Trains a model to detect languages from text and count characters/words
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import os
import re

class MultilingualDetector:
    """Multilingual language detection model with character/word counting capabilities"""
    
    def __init__(self, model_type='logistic'):
        """
        Initialize the detector
        
        Args:
            model_type: Type of classifier ('naive_bayes', 'logistic', 'svm', 'random_forest')
        """
        self.model_type = model_type
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            analyzer='char_wb',  # Character n-grams with word boundaries
            min_df=2,
            max_df=0.95
        )
        self.model = None
        self.label_encoder = {}
        self.labels = []
        
    def train(self, X, y):
        """
        Train the language detection model
        
        Args:
            X: List of text samples
            y: List of language labels
        """
        print(f"Training {self.model_type} model...")
        
        # Create label encoding
        unique_labels = sorted(set(y))
        self.labels = unique_labels
        self.label_encoder = {label: idx for idx, label in enumerate(unique_labels)}
        self.reverse_label_encoder = {idx: label for label, idx in self.label_encoder.items()}
        
        # Encode labels
        y_encoded = [self.label_encoder[label] for label in y]
        
        # Vectorize text
        print("Vectorizing text...")
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # Initialize model based on type
        if self.model_type == 'naive_bayes':
            self.model = MultinomialNB(alpha=0.1)
        elif self.model_type == 'logistic':
            self.model = LogisticRegression(max_iter=1000, random_state=42, C=1.0)
        elif self.model_type == 'svm':
            self.model = SVC(kernel='linear', probability=True, random_state=42)
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
        
        # Train model
        print("Fitting model...")
        self.model.fit(X_vectorized, y_encoded)
        print("Training completed!")
        
    def predict(self, text):
        """
        Predict language from text
        
        Args:
            text: Input text string
            
        Returns:
            Predicted language label
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        X_vectorized = self.vectorizer.transform([text])
        prediction_idx = self.model.predict(X_vectorized)[0]
        return self.reverse_label_encoder[prediction_idx]
    
    def predict_proba(self, text):
        """
        Get prediction probabilities for all languages
        
        Args:
            text: Input text string
            
        Returns:
            Dictionary of language probabilities
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        X_vectorized = self.vectorizer.transform([text])
        probabilities = self.model.predict_proba(X_vectorized)[0]
        
        return {self.reverse_label_encoder[i]: prob for i, prob in enumerate(probabilities)}
    
    def save(self, filepath):
        """Save the trained model to disk"""
        model_data = {
            'vectorizer': self.vectorizer,
            'model': self.model,
            'label_encoder': self.label_encoder,
            'reverse_label_encoder': self.reverse_label_encoder,
            'labels': self.labels,
            'model_type': self.model_type
        }
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"Model saved to {filepath}")
    
    @classmethod
    def load(cls, filepath):
        """Load a trained model from disk"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        detector = cls(model_type=model_data['model_type'])
        detector.vectorizer = model_data['vectorizer']
        detector.model = model_data['model']
        detector.label_encoder = model_data['label_encoder']
        detector.reverse_label_encoder = model_data['reverse_label_encoder']
        detector.labels = model_data['labels']
        
        return detector


def count_characters(text):
    """Count total characters (excluding spaces)"""
    return len(text.replace(' ', ''))


def count_words(text):
    """Count words in text (handles multiple languages)"""
    # Split by whitespace and filter empty strings
    words = [w for w in text.split() if w.strip()]
    return len(words)


def count_letters(text):
    """Count only alphabetic characters (letters)"""
    return len(re.findall(r'[a-zA-Z\u00C0-\u024F\u0370-\u1EFF\u0400-\u04FF\u0600-\u06FF\u0700-\u074F\u0750-\u077F\u0800-\u4DBF\u4E00-\u9FFF\uAC00-\uD7AF]', text))


def analyze_text(text):
    """
    Analyze text and return comprehensive statistics
    
    Returns:
        Dictionary with character counts, word counts, and letter counts
    """
    return {
        'total_characters': len(text),
        'characters_no_spaces': count_characters(text),
        'words': count_words(text),
        'letters': count_letters(text),
        'spaces': text.count(' ')
    }


def load_dataset(csv_path):
    """Load dataset from CSV file"""
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path, encoding='utf-8')
    print(f"Loaded {len(df)} samples")
    print(f"Languages: {df['language'].unique()}")
    print(f"Language distribution:\n{df['language'].value_counts()}")
    return df


def main():
    """Main training function"""
    # Configuration
    CSV_PATH = 'dataset/language_data.csv'
    MODEL_PATH = 'multilingual_detector_model.pkl'
    MODEL_TYPE = 'logistic'  # Options: 'naive_bayes', 'logistic', 'svm', 'random_forest'
    
    # Load dataset
    df = load_dataset(CSV_PATH)
    
    # Prepare data
    X = df['text'].astype(str).tolist()
    y = df['language'].tolist()
    
    # Split data
    print("\nSplitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Train model
    detector = MultilingualDetector(model_type=MODEL_TYPE)
    detector.train(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating model...")
    y_pred = [detector.predict(text) for text in X_test]
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    detector.save(MODEL_PATH)
    
    # Test with sample
    print("\n" + "="*50)
    print("Sample Test:")
    sample_text = X_test[0]
    predicted_lang = detector.predict(sample_text)
    actual_lang = y_test[0]
    stats = analyze_text(sample_text)
    
    # Safe Unicode printing for Windows console
    try:
        text_preview = sample_text[:100]
        print(f"Text: {text_preview}...")
    except UnicodeEncodeError:
        print(f"Text: [Contains non-ASCII characters] (length: {len(sample_text)})")
    
    print(f"Actual Language: {actual_lang}")
    print(f"Predicted Language: {predicted_lang}")
    print(f"Text Statistics:")
    print(f"  - Total Characters: {stats['total_characters']}")
    print(f"  - Characters (no spaces): {stats['characters_no_spaces']}")
    print(f"  - Words: {stats['words']}")
    print(f"  - Letters: {stats['letters']}")
    print(f"  - Spaces: {stats['spaces']}")


if __name__ == '__main__':
    main()
