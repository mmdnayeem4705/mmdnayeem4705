"""
Word/Character Language Detector
Detects which language individual words, characters, or scripts belong to
"""

import os
import re
import sys

class WordLanguageDetector:
    """Detects language for individual words, characters, or scripts"""
    
    def __init__(self, model_path='multilingual_detector_model.pkl'):
        """Initialize with the trained language detection model"""
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}\n"
                f"Please train the model first: python model_trainer.py"
            )
        
        import pickle
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.model = model_data['model']
        self.reverse_label_encoder = model_data['reverse_label_encoder']
        
        print(f"Word Language Detector loaded successfully!")
    
    def detect_word_language(self, word):
        """
        Detect language for a single word or character sequence
        
        Args:
            word: Single word or character sequence (e.g., "书", "libro", "книга")
            
        Returns:
            Dictionary with language and confidence
        """
        if not word or not word.strip():
            return {'language': None, 'confidence': 0.0, 'word': word}
        
        word_clean = word.strip()
        
        # Vectorize
        X_vectorized = self.vectorizer.transform([word_clean])
        
        # Predict
        prediction_idx = self.model.predict(X_vectorized)[0]
        probabilities = self.model.predict_proba(X_vectorized)[0]
        
        predicted_language = self.reverse_label_encoder[prediction_idx]
        confidence = probabilities[prediction_idx]
        
        return {
            'word': word_clean,
            'language': predicted_language,
            'confidence': float(confidence),
            'all_probabilities': {
                self.reverse_label_encoder[i]: float(prob)
                for i, prob in enumerate(probabilities)
            }
        }
    
    def detect_multiple_words(self, words):
        """
        Detect languages for multiple words
        
        Args:
            words: List of words or single string with words separated by commas
            
        Returns:
            List of detection results
        """
        if isinstance(words, str):
            # Parse comma-separated words, handling parentheses
            words = self._parse_word_list(words)
        
        results = []
        for word in words:
            word_clean = word.strip()
            if word_clean:
                result = self.detect_word_language(word_clean)
                results.append(result)
        
        return results
    
    def _parse_word_list(self, text):
        """Parse a string like 'word1, word2 (meaning), word3' into word list"""
        # Remove content in parentheses (translations/meanings)
        text_no_parens = re.sub(r'\([^)]*\)', '', text)
        # Split by commas
        words = [w.strip() for w in text_no_parens.split(',')]
        return [w for w in words if w]
    
    def parse_formatted_input(self, text):
        """
        Parse formatted input with language labels and extract words
        
        Example input format:
        Chinese (中文): 书 (book), 学习 (study)
        French: livre (book), école (school)
        
        Args:
            text: Formatted text with language labels
            
        Returns:
            Dictionary with language sections and their words
        """
        lines = text.split('\n')
        sections = {}
        
        current_language = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line starts with a language label
            # Pattern: "LanguageName (script): words" or "LanguageName: words"
            match = re.match(r'^([^:]+?)(?:\s*\([^)]+\))?:\s*(.+)$', line)
            if match:
                lang_label = match.group(1).strip()
                words_text = match.group(2).strip()
                
                # Clean language label (remove script names in parentheses)
                current_language = re.sub(r'\s*\([^)]+\)', '', lang_label).strip()
                
                # Extract words (remove parentheses with meanings)
                words = self._parse_word_list(words_text)
                sections[current_language] = words
            elif current_language and ':' in line:
                # Continuation line (words after colon)
                words_text = line.split(':', 1)[1].strip()
                if current_language not in sections:
                    sections[current_language] = []
                words = self._parse_word_list(words_text)
                sections[current_language].extend(words)
        
        return sections
    
    def analyze_formatted_input(self, formatted_text):
        """
        Analyze formatted input and detect language for each word
        
        Args:
            formatted_text: Formatted text with language sections
            
        Returns:
            Dictionary with analysis results
        """
        # Parse the formatted input
        sections = self.parse_formatted_input(formatted_text)
        
        results = {
            'sections': [],
            'all_detections': []
        }
        
        for label_language, words in sections.items():
            section_results = {
                'label': label_language,
                'words': []
            }
            
            for word in words:
                detection = self.detect_word_language(word)
                section_results['words'].append(detection)
                results['all_detections'].append({
                    'word': word,
                    'label_language': label_language,
                    'detected_language': detection['language'],
                    'confidence': detection['confidence']
                })
            
            results['sections'].append(section_results)
        
        return results


def print_detection_result(result, show_probabilities=False):
    """Print a single detection result"""
    print(f"  Word: {result['word']}")
    print(f"    → Detected Language: {result['language']}")
    print(f"    → Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
    
    if show_probabilities and 'all_probabilities' in result:
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        print(f"    → Top probabilities: {', '.join([f'{lang}({prob:.2f})' for lang, prob in sorted_probs])}")


def print_formatted_analysis(analysis_results, show_probabilities=False):
    """Print formatted analysis results"""
    print("\n" + "="*70)
    print("LANGUAGE DETECTION RESULTS")
    print("="*70)
    
    for section in analysis_results['sections']:
        print(f"\n{section['label']}:")
        print("-" * 70)
        
        for word_result in section['words']:
            print_detection_result(word_result, show_probabilities)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    # Count correct/incorrect detections
    correct = 0
    total = 0
    
    for item in analysis_results['all_detections']:
        total += 1
        label_lang = item['label_language'].lower()
        detected_lang = item['detected_language'].lower()
        
        # Check if detected language matches label (with fuzzy matching)
        if detected_lang in label_lang or label_lang in detected_lang:
            correct += 1
        elif item['confidence'] > 0.9:  # High confidence might indicate correct
            correct += 1
    
    print(f"\nTotal words analyzed: {total}")
    print(f"Detections with high confidence (>0.9): {sum(1 for d in analysis_results['all_detections'] if d['confidence'] > 0.9)}")
    
    # Show all detected languages
    detected_langs = {}
    for item in analysis_results['all_detections']:
        lang = item['detected_language']
        detected_langs[lang] = detected_langs.get(lang, 0) + 1
    
    print(f"\nLanguages detected: {', '.join(sorted(detected_langs.keys()))}")


def main():
    """Main function - can be used interactively or with file input"""
    # Check if model exists
    model_path = 'multilingual_detector_model.pkl'
    
    if not os.path.exists(model_path):
        print("ERROR: Model not found!")
        print("Please train the model first: python model_trainer.py")
        return
    
    # Initialize detector
    try:
        detector = WordLanguageDetector(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    print("\n" + "="*70)
    print("WORD/CHARACTER LANGUAGE DETECTOR")
    print("="*70)
    print("\nOptions:")
    print("  1. Enter formatted text (with language labels)")
    print("  2. Enter single word/character to detect")
    print("  3. Enter multiple words separated by commas")
    print("  4. Type 'file:<filename>' to read from file")
    print("  5. Type 'quit' to exit")
    print("="*70)
    
    while True:
        print("\n" + "-"*70)
        user_input = input("\nEnter text (or 'help' for options, 'quit' to exit): ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if user_input.lower() == 'help':
            print("\n" + "="*70)
            print("HELP")
            print("="*70)
            print("\nFormatted Input Example:")
            print("  Chinese (中文): 书 (book), 学习 (study)")
            print("  French: livre (book), école (school)")
            print("\nSingle Word:")
            print("  书")
            print("\nMultiple Words:")
            print("  书, livre, книга")
            print("="*70)
            continue
        
        # Check for file input
        if user_input.startswith('file:'):
            filename = user_input[5:].strip()
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    user_input = f.read()
                print(f"\nFile loaded: {filename}")
            except Exception as e:
                print(f"Error reading file: {e}")
                continue
        
        try:
            # Try to detect if it's formatted input (has language labels)
            if ':' in user_input and '\n' in user_input:
                # Formatted input with language labels
                print("\nAnalyzing formatted input...")
                results = detector.analyze_formatted_input(user_input)
                print_formatted_analysis(results, show_probabilities=False)
            
            elif ',' in user_input and ':' not in user_input:
                # Multiple words separated by commas
                print("\nDetecting languages for multiple words...")
                results = detector.detect_multiple_words(user_input)
                
                print("\n" + "="*70)
                print("DETECTION RESULTS")
                print("="*70)
                for result in results:
                    print_detection_result(result, show_probabilities=False)
            
            else:
                # Single word
                print("\nDetecting language for word...")
                result = detector.detect_word_language(user_input)
                
                print("\n" + "="*70)
                print("DETECTION RESULT")
                print("="*70)
                print_detection_result(result, show_probabilities=True)
        
        except Exception as e:
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()


# Example usage with the provided format
def example_usage():
    """Example usage with the user's provided format"""
    sample_text = """Chinese (中文): 书 (book), 学习 (study), 朋友 (friend)

Finnish: kirja (book), koulu (school), ystävä (friend)

French: livre (book), école (school), ami (friend)

Greek (Ελληνικά): βιβλίο (book), σχολείο (school), φίλος (friend)

Gujarati (ગુજરાતી): પુસ્તક (book), શાળા (school), મિત્ર (friend)

Hindi (हिन्दी): किताब (book), स्कूल (school), दोस्त (friend)

Indonesian: buku (book), sekolah (school), teman (friend)

Korean (한국어): 책 (book), 학교 (school), 친구 (friend)

Malay: buku (book), sekolah (school), kawan (friend)

Italian: libro (book), scuola (school), amico (friend)

Urdu (اردو): کتاب (book), اسکول (school), دوست (friend)

Tagalog: aklat (book), paaralan (school), kaibigan (friend)

Swedish: bok (book), skola (school), vän (friend)

Spanish: libro (book), escuela (school), amigo (friend)

Telugu (తెలుగు): పుస్తకం (book), పాఠశాల (school), స్నేహితుడు (friend)

Tamil (தமிழ்): புத்தகம் (book), பள்ளி (school), நண்பன் (friend)

Marathi (मराठी): पुस्तक (book), शाळा (school), मित्र (friend)

Nepali (नेपाली): किताब (book), विद्यालय (school), साथी (friend)

Persian (فارسی): کتاب (book), مدرسه (school), دوست (friend)

Polish: książka (book), szkoła (school), przyjaciel (friend)

Portuguese: livro (book), escola (school), amigo (friend)

Russian (Русский): книга (book), школа (school), друг (friend)"""
    
    if os.path.exists('multilingual_detector_model.pkl'):
        detector = WordLanguageDetector()
        results = detector.analyze_formatted_input(sample_text)
        print_formatted_analysis(results, show_probabilities=False)
    else:
        print("Model not found. Please train first: python model_trainer.py")


if __name__ == '__main__':
    # Set UTF-8 encoding for Windows
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass
    
    # Run main interactive mode
    main()
