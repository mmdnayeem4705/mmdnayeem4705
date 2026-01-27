"""
Interactive Language Detector
Allows users to input text and see language detection and statistics output
"""

import os
import sys

def safe_print(text):
    """Safely print Unicode text on Windows"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Try UTF-8 encoding
        try:
            print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
        except:
            print("[Text contains unsupported Unicode characters]")

def main():
    """Interactive language detection interface"""
    
    # Check if model exists
    model_path = 'multilingual_detector_model.pkl'
    
    if not os.path.exists(model_path):
        print("="*70)
        print("ERROR: Model not found!")
        print("="*70)
        print("Please train the model first by running:")
        print("  python model_trainer.py")
        print("\nThis will create the required model file.")
        return
    
    # Import detector after checking model exists
    try:
        from language_detector import LanguageDetector
    except ImportError as e:
        print(f"Error importing LanguageDetector: {e}")
        print("Please make sure language_detector.py is in the same directory.")
        return
    
    # Initialize detector
    print("="*70)
    print("MULTILINGUAL LANGUAGE DETECTOR - INTERACTIVE MODE")
    print("="*70)
    print("\nLoading model...")
    
    try:
        detector = LanguageDetector(model_path)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
        return
    
    print("\n" + "="*70)
    print("Ready! Enter text to detect language and get statistics.")
    print("Type 'quit' or 'exit' to stop, 'help' for more options.")
    print("="*70)
    
    while True:
        print("\n" + "-"*70)
        user_input = input("\nEnter text (or 'help' for options, 'quit' to exit): ").strip()
        
        if not user_input:
            print("Please enter some text.")
            continue
        
        # Handle commands
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye!")
            break
        
        if user_input.lower() == 'help':
            print("\n" + "="*70)
            print("HELP - Available Commands:")
            print("="*70)
            print("  'quit' or 'exit' - Exit the program")
            print("  'help' - Show this help message")
            print("  'prob' - Toggle probability display (type 'prob' before entering text)")
            print("  'multi' - Enter multi-line mode (type 'multi' before entering text)")
            print("\nExamples:")
            print("  - Enter any text to detect its language")
            print("  - Type 'prob' then enter text to see all language probabilities")
            print("  - Type 'multi' to analyze multiple lines/pages")
            print("="*70)
            continue
        
        # Special modes
        show_probabilities = False
        multi_line_mode = False
        
        if user_input.lower() == 'prob':
            show_probabilities = True
            print("\nProbability mode enabled. Enter your text:")
            user_input = input("> ").strip()
            if not user_input:
                continue
        
        if user_input.lower() == 'multi':
            multi_line_mode = True
            print("\nMulti-line mode enabled. Enter your text (press Enter twice to finish):")
            lines = []
            while True:
                line = input()
                if line == "" and lines:  # Empty line after text
                    break
                if line:
                    lines.append(line)
            user_input = "\n".join(lines)
            if not user_input.strip():
                print("No text entered.")
                continue
        
        # Analyze the text
        try:
            if multi_line_mode:
                result = detector.analyze_page(user_input, include_probabilities=show_probabilities)
                
                print("\n" + "="*70)
                print("ANALYSIS RESULTS")
                print("="*70)
                
                print(f"\nOverall Detected Language: {result['detected_language']}")
                print(f"Confidence: {result['confidence']:.4f}")
                
                if 'languages_present' in result:
                    print(f"Languages Found in Page: {', '.join(result['languages_present'])}")
                
                stats = result['statistics']
                print(f"\nOverall Statistics:")
                print(f"  • Total Characters: {stats['total_characters']}")
                print(f"  • Characters (no spaces): {stats['characters_no_spaces']}")
                print(f"  • Total Letters: {stats['letters']}")
                print(f"  • Total Words: {stats['words']}")
                print(f"  • Spaces: {stats['spaces']}")
                print(f"  • Lines: {stats['lines']}")
                
                if show_probabilities and 'all_probabilities' in result:
                    print(f"\nAll Language Probabilities:")
                    sorted_probs = sorted(
                        result['all_probabilities'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    for lang, prob in sorted_probs:
                        if prob > 0.001:  # Only show probabilities > 0.1%
                            print(f"  • {lang}: {prob:.4f} ({prob*100:.2f}%)")
                
                if 'line_breakdown' in result and result['line_breakdown']:
                    print(f"\nLine-by-Line Breakdown:")
                    print("-"*70)
                    for line_info in result['line_breakdown']:
                        print(f"\nLine {line_info['line_number']}:")
                        try:
                            preview = line_info['text'][:60] + "..." if len(line_info['text']) > 60 else line_info['text']
                            safe_print(f"  Text: {preview}")
                        except:
                            print(f"  Text: [Line {line_info['line_number']}]")
                        print(f"  Language: {line_info['language']} (confidence: {line_info['confidence']:.4f})")
                        print(f"  Letters: {line_info['letter_count']}, Words: {line_info['word_count']}, Characters: {line_info['character_count']}")
            
            else:
                result = detector.analyze(user_input, include_probabilities=show_probabilities)
                
                print("\n" + "="*70)
                print("ANALYSIS RESULTS")
                print("="*70)
                
                print(f"\nDetected Language: {result['detected_language']}")
                print(f"Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)")
                
                stats = result['statistics']
                print(f"\nText Statistics:")
                print(f"  • Total Characters: {stats['total_characters']}")
                print(f"  • Characters (no spaces): {stats['characters_no_spaces']}")
                print(f"  • Letters: {stats['letters']}")
                print(f"  • Words: {stats['words']}")
                print(f"  • Spaces: {stats['spaces']}")
                
                if show_probabilities and 'all_probabilities' in result:
                    print(f"\nAll Language Probabilities:")
                    sorted_probs = sorted(
                        result['all_probabilities'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:10]  # Show top 10
                    for lang, prob in sorted_probs:
                        if prob > 0.001:  # Only show probabilities > 0.1%
                            print(f"  • {lang}: {prob:.4f} ({prob*100:.2f}%)")
        
        except Exception as e:
            print(f"\nError analyzing text: {e}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    # Set UTF-8 encoding for Windows console if possible
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except:
            pass  # If we can't change encoding, continue with default
    
    main()
