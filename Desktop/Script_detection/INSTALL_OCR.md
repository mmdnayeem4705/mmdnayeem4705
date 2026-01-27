# OCR Installation Guide

To use image text extraction features, you need to install an OCR (Optical Character Recognition) library.

## Option 1: EasyOCR (Recommended - Easiest)

EasyOCR is easier to install and doesn't require system-level installations.

```bash
python -m pip install easyocr
```

**Note:** If `pip` doesn't work, use `python -m pip` instead.

**Note:** First run will download language models (~500MB), which may take a few minutes.

**Pros:**
- Easy installation
- No system dependencies
- Good accuracy for multiple languages
- Works out of the box

**Cons:**
- Larger download (~500MB models)
- Slower than Tesseract

## Option 2: Tesseract OCR

Tesseract requires both Python package and system installation.

### Step 1: Install Python packages
```bash
python -m pip install pytesseract pillow opencv-python
```

### Step 2: Install Tesseract OCR

**Windows:**
1. Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer
3. Note the installation path (usually `C:\Program Files\Tesseract-OCR`)
4. Add Tesseract to PATH or set path in code:
   ```python
   import pytesseract
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

**Pros:**
- Faster than EasyOCR
- Widely used and stable
- Good for common languages

**Cons:**
- Requires system installation
- More setup steps
- Windows installation can be tricky

## Quick Test

After installation, test OCR:

```bash
python image_ocr.py <path_to_image>
```

## GUI Usage

The GUI will automatically try EasyOCR first, then fallback to Tesseract if available.

If neither is installed, the GUI will show an error message with installation instructions when you try to upload an image.
