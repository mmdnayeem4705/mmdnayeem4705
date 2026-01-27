# GUI Application Usage Guide

## Starting the GUI

```bash
python gui_detector.py
```

A window will pop up with the following interface:

## Interface Overview

### 1. Upload Buttons (Top)
- **Upload Text File (.txt)**: Click to select and load a text file
- **Upload Image File (.jpg, .png, .jpeg)**: Click to select an image file. The GUI will automatically extract text using OCR

### 2. Text Input Area
- You can directly type or paste text here
- Text from uploaded files will appear here
- Extracted text from images will appear here

### 3. Detect Language Button
- Click to process the text in the input area
- Detects language and counts letters/words/characters

### 4. Results Area (Bottom)
- Shows detected language
- Shows confidence score
- Shows text statistics (letters, words, characters)
- Displays extracted text preview

### 5. Status Bar
- Shows current status (file loaded, processing, ready, etc.)

## Usage Examples

### Example 1: Upload Text File
1. Click "Upload Text File (.txt)"
2. Select a text file
3. Text appears in the input area
4. Click "Detect Language"
5. Results appear in the results area

### Example 2: Upload Image
1. Click "Upload Image File"
2. Select an image file (must contain text)
3. Wait for OCR to extract text (may take a few seconds)
4. Extracted text appears in the input area
5. Click "Detect Language"
6. Results show detected language and statistics

### Example 3: Direct Text Input
1. Type or paste text directly into the text input area
2. Click "Detect Language"
3. Results appear instantly

### Example 4: Multi-language Text
1. Paste text with multiple languages:
   ```
   Hello world
   Hola mundo
   Bonjour le monde
   ```
2. Click "Detect Language"
3. Results show the primary detected language and overall statistics

## OCR Requirements

For image upload to work, you need OCR installed. The GUI will try:
1. EasyOCR first (if installed)
2. Tesseract OCR as fallback (if installed)

If neither is installed, you'll see an error message with installation instructions.

**Quick Install:**
```bash
pip install easyocr
```

## Keyboard Shortcuts

- **Ctrl+V**: Paste text (standard)
- **Ctrl+A**: Select all text (standard)
- **Ctrl+C**: Copy (standard)

## Troubleshooting

### "Model not found" Error
- Train the model first: `python model_trainer.py`

### "OCR not available" Error
- Install OCR: `pip install easyocr`
- Or see `INSTALL_OCR.md` for detailed instructions

### Image text extraction fails
- Make sure image has clear, readable text
- Try higher resolution images
- Check OCR is installed correctly

### GUI doesn't open
- Make sure you have Python with Tkinter (usually comes with Python)
- On Linux: `sudo apt-get install python3-tk`

## Features

✅ **Text File Upload**: Support for .txt files  
✅ **Image Upload**: Support for .jpg, .png, .jpeg with OCR  
✅ **Direct Text Input**: Type or paste text directly  
✅ **Language Detection**: Detects 22+ languages  
✅ **Statistics**: Letter count, word count, character count  
✅ **Multi-language Support**: Handles Unicode characters  
✅ **Real-time Processing**: Instant results  

## Output Format

The results show:
- **Detected Language**: The most likely language
- **Confidence**: How confident the model is (0-1, or 0-100%)
- **Total Characters**: All characters including spaces
- **Characters (no spaces)**: All characters excluding spaces
- **Letters**: Only alphabetic characters (Unicode supported)
- **Words**: Word count (space-separated)
- **Spaces**: Number of spaces
- **Lines**: Number of lines
