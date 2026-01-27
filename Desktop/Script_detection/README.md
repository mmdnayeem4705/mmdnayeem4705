# Multilingual Language Detection and Text Analysis

A machine learning model that detects languages from text and provides comprehensive text analysis including letter, word, and character counting. Supports 22+ languages including Chinese, Spanish, French, Hindi, Korean, and many more.

## Features

- **Language Detection**: Automatically detects the language of input text from 22+ supported languages
- **Text Statistics**: Counts letters, words, characters (with/without spaces)
- **Multi-line Analysis**: Analyzes entire pages with line-by-line breakdown
- **High Accuracy**: Uses TF-IDF vectorization with logistic regression classifier
- **Confidence Scores**: Provides confidence scores for language predictions
- **Multiple Languages on One Page**: Can identify different languages in different parts of a document

## Supported Languages

The model supports the following languages (from the dataset):
- Chinese
- Finnish
- French
- Greek
- Gujarati
- Hindi
- Indonesian
- Korean
- Malay
- Italian
- Urdu
- Tagalog
- Swedish
- Spanish
- Telugu
- Tamil
- Marathi
- Nepali
- Persian
- Polish
- Portuguese
- Russian

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Train the Model

First, train the model using your dataset:

```bash
python model_trainer.py
```

This will:
- Load the dataset from `dataset/language_data.csv`
- Train a language detection model
- Save the trained model to `multilingual_detector_model.pkl`
- Display training accuracy and evaluation metrics

**Model Options**: You can modify the `MODEL_TYPE` in `model_trainer.py` to use different classifiers:
- `'logistic'` - Logistic Regression (default, good balance)
- `'naive_bayes'` - Naive Bayes (fast, good for text)
- `'svm'` - Support Vector Machine (slower but often more accurate)
- `'random_forest'` - Random Forest (good for complex patterns)

### Step 2: Use the Model

#### Python API Usage

```python
from language_detector import LanguageDetector

# Initialize detector
detector = LanguageDetector('multilingual_detector_model.pkl')

# Analyze a single text
text = "Hello, how are you today?"
result = detector.analyze(text)

print(f"Language: {result['detected_language']}")
print(f"Confidence: {result['confidence']:.4f}")
print(f"Letters: {result['statistics']['letters']}")
print(f"Words: {result['statistics']['words']}")
print(f"Characters: {result['statistics']['characters_no_spaces']}")

# Analyze a full page with multiple languages
page_text = """Hello, this is English.
Hola, esto es español.
Bonjour, ceci est français."""

page_result = detector.analyze_page(page_text)
print(f"Languages found: {page_result['languages_present']}")
```

#### Interactive Usage (Input/Output)

For an interactive experience where you can input text and see results:

```bash
python interactive_detector.py
```

This will start an interactive session where you can:
- Enter text to detect language and get statistics
- Type `prob` before entering text to see all language probabilities
- Type `multi` to analyze multi-line pages with line-by-line breakdown
- Type `help` for more options
- Type `quit` to exit

#### Command Line Usage

Run the example script to see the detector in action:

```bash
python language_detector.py
```

## Model Architecture

The model uses:
- **TF-IDF Vectorization**: Character n-grams (1-3) with word boundaries
- **Logistic Regression**: Multi-class classifier for language prediction
- **Stratified Train-Test Split**: 80% training, 20% testing

## Output Format

The analyzer returns a dictionary with:

```python
{
    'detected_language': 'English',
    'confidence': 0.95,
    'statistics': {
        'total_characters': 100,
        'characters_no_spaces': 85,
        'words': 15,
        'letters': 80,
        'spaces': 15,
        'lines': 1
    },
    'all_probabilities': {  # if include_probabilities=True
        'English': 0.95,
        'Spanish': 0.03,
        ...
    }
}
```

For page analysis, additional fields include:
- `line_breakdown`: Per-line analysis with language and statistics
- `languages_present`: List of all languages found in the page
- `language_distribution`: Count of lines per language

## Dataset

The model is trained on `dataset/language_data.csv` which contains:
- `text`: Sample text in various languages
- `language`: Language label

Make sure your dataset follows this format.

## File Structure

```
Script_detection/
├── dataset/
│   └── language_data.csv          # Training dataset
├── model_trainer.py               # Model training script
├── language_detector.py           # Detection and analysis API
├── interactive_detector.py        # Interactive input/output interface
├── example_usage.py               # Example usage script
├── multilingual_detector_model.pkl # Trained model (generated after training)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## Example Use Cases

1. **Document Language Detection**: Identify the language of documents
2. **Multi-language Content Analysis**: Analyze pages with mixed languages
3. **Text Statistics**: Count letters, words, and characters for content analysis
4. **Content Filtering**: Filter content by detected language
5. **Translation Workflows**: Identify source language before translation

## Performance

Typical performance metrics:
- **Accuracy**: >95% on test set (varies by dataset)
- **Inference Speed**: <100ms per text sample
- **Memory Usage**: ~50-100MB for the trained model

## Troubleshooting

**Error: Model file not found**
- Solution: Run `python model_trainer.py` first to train the model

**Unicode/Encoding Errors**
- Ensure your dataset CSV is UTF-8 encoded
- The code handles Unicode characters automatically

**Low Accuracy**
- Try different model types (SVM often performs better)
- Check if your dataset is balanced across languages
- Increase training data if possible

## License

This project is provided as-is for educational and development purposes.
