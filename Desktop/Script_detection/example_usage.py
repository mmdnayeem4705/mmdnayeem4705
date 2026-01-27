"""
Example usage script demonstrating language detection and text analysis
"""

from language_detector import LanguageDetector, analyze_text

def main():
    # Check if model exists
    import os
    model_path = 'multilingual_detector_model.pkl'
    
    if not os.path.exists(model_path):
        print("="*60)
        print("ERROR: Model not found!")
        print("="*60)
        print("Please train the model first by running:")
        print("  python model_trainer.py")
        print("\nThis will create the required model file.")
        return
    
    # Initialize detector
    print("="*60)
    print("Initializing Language Detector...")
    print("="*60)
    detector = LanguageDetector(model_path)
    
    # Example 1: Single language text
    print("\n" + "="*60)
    print("EXAMPLE 1: Single Language Detection")
    print("="*60)
    
    texts = [
        ("English", "Hello, how are you today? This is a sample English text."),
        ("Spanish", "Hola, ¿cómo estás hoy? Este es un texto de ejemplo en español."),
        ("French", "Bonjour, comment allez-vous aujourd'hui? Ceci est un texte d'exemple en français."),
        ("Hindi", "नमस्ते, आज आप कैसे हैं? यह हिंदी में एक उदाहरण पाठ है।"),
        ("Chinese", "你好，你今天怎么样？这是一个中文示例文本。"),
        ("Korean", "안녕하세요, 오늘 어떻게 지내세요? 이것은 한국어 예제 텍스트입니다."),
    ]
    
    for lang_name, text in texts:
        print(f"\n--- {lang_name} ---")
        print(f"Text: {text}")
        result = detector.analyze(text, include_probabilities=False)
        print(f"Detected Language: {result['detected_language']} (confidence: {result['confidence']:.4f})")
        stats = result['statistics']
        print(f"  Letters: {stats['letters']}")
        print(f"  Words: {stats['words']}")
        print(f"  Characters (no spaces): {stats['characters_no_spaces']}")
    
    # Example 2: Multi-language page
    print("\n" + "="*60)
    print("EXAMPLE 2: Multi-Language Page Analysis")
    print("="*60)
    
    page_text = """Hello, this is an English paragraph. It contains several sentences.
This is another English sentence.

Hola, este es un párrafo en español. Contiene varias oraciones.
Esta es otra oración en español.

Bonjour, ceci est un paragraphe en français. Il contient plusieurs phrases.
Ceci est une autre phrase en français."""
    
    print("\nPage Text:")
    print("-" * 60)
    print(page_text)
    print("-" * 60)
    
    page_result = detector.analyze_page(page_text, include_probabilities=False)
    
    print(f"\nOverall Analysis:")
    print(f"  Primary Language: {page_result['detected_language']}")
    print(f"  Languages Present: {', '.join(page_result.get('languages_present', []))}")
    
    overall_stats = page_result['statistics']
    print(f"\nOverall Statistics:")
    print(f"  Total Letters: {overall_stats['letters']}")
    print(f"  Total Words: {overall_stats['words']}")
    print(f"  Total Characters (no spaces): {overall_stats['characters_no_spaces']}")
    print(f"  Total Spaces: {overall_stats['spaces']}")
    
    if 'line_breakdown' in page_result:
        print(f"\nLine-by-Line Breakdown:")
        for line_info in page_result['line_breakdown']:
            if line_info['text'].strip():  # Only show non-empty lines
                print(f"  Line {line_info['line_number']}:")
                print(f"    Text: {line_info['text'][:50]}...")
                print(f"    Language: {line_info['language']} (confidence: {line_info['confidence']:.4f})")
                print(f"    Letters: {line_info['letter_count']}, Words: {line_info['word_count']}")
    
    # Example 3: Detailed probability analysis
    print("\n" + "="*60)
    print("EXAMPLE 3: Detailed Probability Analysis")
    print("="*60)
    
    sample_text = "Hello world, this is a test sentence."
    result = detector.analyze(sample_text, include_probabilities=True)
    
    print(f"\nText: {sample_text}")
    print(f"Detected Language: {result['detected_language']} (confidence: {result['confidence']:.4f})")
    
    if 'all_probabilities' in result:
        print("\nTop 5 Language Probabilities:")
        sorted_probs = sorted(
            result['all_probabilities'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for lang, prob in sorted_probs:
            print(f"  {lang}: {prob:.4f}")
    
    # Example 4: Letter and word counting only (without model)
    print("\n" + "="*60)
    print("EXAMPLE 4: Text Statistics (No Model Required)")
    print("="*60)
    
    test_text = "Hello, this is a test! 123"
    stats = analyze_text(test_text)
    
    print(f"\nText: {test_text}")
    print(f"Statistics:")
    print(f"  Total Characters: {stats['total_characters']}")
    print(f"  Characters (no spaces): {stats['characters_no_spaces']}")
    print(f"  Letters: {stats['letters']}")
    print(f"  Words: {stats['words']}")
    print(f"  Spaces: {stats['spaces']}")


if __name__ == '__main__':
    main()
