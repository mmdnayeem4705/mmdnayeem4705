# Quick Start Commands

## Step 1: Install Dependencies (First time only)

### Basic Installation (for text detection only)
```bash
python -m pip install -r requirements.txt
```

### For Image OCR Support (optional but recommended)
Choose one:

**Option A: EasyOCR (Recommended - Easy Setup)**
```bash
python -m pip install easyocr
```

**Option B: Tesseract OCR**
```bash
python -m pip install pytesseract pillow opencv-python
# Then install Tesseract system package (see INSTALL_OCR.md)
```

**Note:** If `pip` doesn't work, always use `python -m pip` instead.

See `INSTALL_OCR.md` for detailed OCR installation instructions.

## Step 2: Train the Model (First time only, or to retrain)
```bash
python model_trainer.py
```

## Step 3: Use the Model

### Option A: GUI Application (Recommended - Upload Text or Images!)
```bash
python gui_detector.py
```
**Open a window to:**
- Upload text files (.txt)
- Upload image files (.jpg, .png, .jpeg) - automatically extracts text using OCR
- Enter text directly in the text box
- See language detection results with statistics

### Option B: Word/Character Language Detector (For individual words/scripts)
```bash
python word_language_detector.py
```
Perfect for detecting which language individual words or characters belong to!

### Option B: Full Text Language Detector (Interactive Mode)
```bash
python interactive_detector.py
```
For detecting language of sentences/paragraphs and getting statistics.

### Option C: Test with Example
```bash
python test_word_detector.py
```
Runs the word detector with a pre-loaded example.

### Option D: Run Example Scripts
```bash
python example_usage.py
```

## Quick Reference for Word Language Detector

Once you run `python word_language_detector.py`:

**Detect single word:**
- Just type: `书` or `libro` or `книга`

**Detect multiple words:**
- Type: `书, livre, книга`

**Detect formatted input (with language labels):**
- Type or paste your formatted text like:
```
Chinese (中文): 书 (book), 学习 (study)
French: livre (book), école (school)
```

**Other commands:**
- Type `help` for more options
- Type `file:<filename>` to read from file
- Type `quit` to exit

## Quick Reference for Interactive Mode

Once you run `python interactive_detector.py`:
- Just type your text and press Enter to see results
- Type `prob` then Enter, then your text to see all language probabilities
- Type `multi` then Enter to analyze multiple lines
- Type `help` for more options
- Type `quit` to exit
