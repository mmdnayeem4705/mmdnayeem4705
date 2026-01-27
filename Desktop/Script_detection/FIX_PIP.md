# Fixing pip Installation Issues

## Problem

If you see this error:
```
Fatal error in launcher: Unable to create process using '...python.exe'
```

This means `pip` is pointing to a Python version that doesn't exist.

## Solution

**Always use `python -m pip` instead of `pip`**

## Examples

❌ **Don't use:**
```bash
pip install easyocr
```

✅ **Use instead:**
```bash
python -m pip install easyocr
```

## All Installation Commands

### Basic requirements
```bash
python -m pip install -r requirements.txt
```

### Install EasyOCR
```bash
python -m pip install easyocr
```

### Install Tesseract packages
```bash
python -m pip install pytesseract pillow opencv-python
```

### Install individual packages
```bash
python -m pip install pandas numpy scikit-learn
```

## Why This Works

`python -m pip` uses the Python interpreter that's currently active in your terminal, ensuring it uses the correct Python version. The standalone `pip` command may point to a different (or missing) Python installation.

## Quick Check

To verify Python and pip are working:

```bash
python --version
python -m pip --version
```

Both should work without errors.
