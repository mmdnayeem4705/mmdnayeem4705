"""
Test script for word language detector with the provided example
"""

import os
import sys

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass

from word_language_detector import WordLanguageDetector, print_formatted_analysis

def main():
    # Check if model exists
    model_path = 'multilingual_detector_model.pkl'
    
    if not os.path.exists(model_path):
        print("ERROR: Model not found!")
        print("Please train the model first: python model_trainer.py")
        return
    
    print("="*70)
    print("TESTING WORD LANGUAGE DETECTOR")
    print("="*70)
    print("\nLoading model...")
    
    try:
        detector = WordLanguageDetector(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    # Test with the provided example
    test_input = """Chinese (中文): 书 (book), 学习 (study), 朋友 (friend)

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
    
    print("\nAnalyzing test input...")
    print("-"*70)
    
    results = detector.analyze_formatted_input(test_input)
    print_formatted_analysis(results, show_probabilities=False)

if __name__ == '__main__':
    main()
