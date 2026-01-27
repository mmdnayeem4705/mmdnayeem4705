"""
OCR (Optical Character Recognition) Module
Extracts text from images for language detection
"""

import os
import sys

try:
    import pytesseract
    from PIL import Image
    import cv2
    import numpy as np
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class ImageOCR:
    """Extract text from images using OCR"""
    
    def __init__(self, ocr_engine='tesseract'):
        """
        Initialize OCR
        
        Args:
            ocr_engine: 'tesseract' or 'easyocr'
        """
        self.ocr_engine = ocr_engine
        self.easyocr_reader = None
        
        if ocr_engine == 'tesseract' and not OCR_AVAILABLE:
            raise ImportError(
                "Tesseract OCR not available. Install with:\n"
                "  pip install pytesseract pillow opencv-python\n"
                "And install Tesseract: https://github.com/tesseract-ocr/tesseract/wiki"
            )
        
        if ocr_engine == 'easyocr' and not EASYOCR_AVAILABLE:
            raise ImportError(
                "EasyOCR not available. Install with:\n"
                "  pip install easyocr"
            )
        
        # Initialize EasyOCR if selected
        if ocr_engine == 'easyocr' and EASYOCR_AVAILABLE:
            print("Initializing EasyOCR... (this may take a moment on first run)")
            try:
                # Try multilingual support first
                try:
                    # Use multiple languages for better multilingual support
                    self.easyocr_reader = easyocr.Reader(['en', 'ch_sim'], gpu=False)
                    print("EasyOCR initialized with multilingual support (English + Chinese)!")
                except:
                    # Fallback to English only if multilingual fails
                    self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
                    print("EasyOCR initialized with English support!")
            except Exception as e:
                print(f"Warning: EasyOCR initialization failed: {e}")
                print("Falling back to Tesseract if available...")
                if OCR_AVAILABLE:
                    self.ocr_engine = 'tesseract'
                else:
                    raise
    
    def preprocess_image(self, image_path, method='adaptive'):
        """
        Preprocess image for better OCR results
        
        Args:
            image_path: Path to image file
            method: 'adaptive', 'otsu', 'gaussian', or 'combined'
            
        Returns:
            Preprocessed image
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # Resize if too small (helps with low-res images)
        height, width = gray.shape
        if width < 300 or height < 300:
            scale = max(300 / width, 300 / height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        
        # Apply different preprocessing methods
        if method == 'adaptive':
            # Adaptive thresholding (good for varying lighting)
            thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == 'otsu':
            # Otsu's thresholding (good for bimodal images)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif method == 'gaussian':
            # Gaussian blur + Otsu
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif method == 'combined':
            # Try multiple and return best
            # First denoise
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            # Then adaptive threshold
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        else:
            thresh = gray
        
        # Additional morphological operations to clean up
        kernel = np.ones((1, 1), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return thresh
    
    def clean_ocr_text(self, text):
        """
        Clean OCR text to remove common artifacts and errors
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        if not text:
            return text
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove lines that are too short or likely noise
            if len(line.strip()) < 2:
                continue
            
            # Remove common OCR artifacts
            line = line.replace('|', 'I').replace('0', 'O')  # Common OCR mistakes
            line = line.replace('®', '').replace('©', '')  # Remove symbols
            
            # Remove excessive whitespace
            line = ' '.join(line.split())
            
            if line.strip():
                cleaned_lines.append(line)
        
        # Join lines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove excessive newlines
        cleaned_text = '\n'.join([line for line in cleaned_text.split('\n') if line.strip()])
        
        return cleaned_text.strip()
    
    def extract_text_tesseract(self, image_path, preprocess=True, psm_mode=6):
        """
        Extract text using Tesseract OCR
        
        Args:
            image_path: Path to image file
            preprocess: Whether to preprocess image
            psm_mode: Page segmentation mode (6=uniform block, 3=auto, 11=sparse text)
            
        Returns:
            Extracted text string
        """
        if not OCR_AVAILABLE:
            raise ImportError("Tesseract OCR not available")
        
        try:
            best_text = None
            best_length = 0
            
            # Try different preprocessing methods
            preprocess_methods = ['adaptive', 'otsu', 'combined'] if preprocess else [None]
            
            for preprocess_method in preprocess_methods:
                try:
                    if preprocess_method:
                        processed_img = self.preprocess_image(image_path, method=preprocess_method)
                        pil_img = Image.fromarray(processed_img)
                    else:
                        pil_img = Image.open(image_path)
                    
                    # Try different PSM modes if initial doesn't work well
                    psm_modes = [psm_mode, 3, 11, 6] if psm_mode else [3, 11, 6]
                    
                    for psm in psm_modes:
                        try:
                            custom_config = f'--oem 3 --psm {psm} -c tessedit_char_whitelist='
                            # Extract text
                            text = pytesseract.image_to_string(pil_img, config=custom_config)
                            text = self.clean_ocr_text(text)
                            
                            # Keep the longest valid result
                            if len(text) > best_length:
                                best_text = text
                                best_length = len(text)
                        except:
                            continue
                
                except Exception as e:
                    continue
            
            if best_text:
                return best_text
            else:
                # Fallback to simple extraction
                pil_img = Image.open(image_path)
                text = pytesseract.image_to_string(pil_img, config='--oem 3 --psm 6')
                return self.clean_ocr_text(text).strip()
        
        except Exception as e:
            raise Exception(f"Tesseract OCR failed: {e}")
    
    def extract_text_easyocr(self, image_path, confidence_threshold=0.5):
        """
        Extract text using EasyOCR
        
        Args:
            image_path: Path to image file
            confidence_threshold: Minimum confidence (0-1) for accepting text
            
        Returns:
            Extracted text string
        """
        if not EASYOCR_AVAILABLE or self.easyocr_reader is None:
            raise ImportError("EasyOCR not available")
        
        try:
            # Read image with confidence scores
            results = self.easyocr_reader.readtext(image_path)
            
            # Filter by confidence and combine text
            text_lines = []
            for result in results:
                # result format: (bbox, text, confidence)
                if len(result) >= 3:
                    confidence = result[2]
                    text = result[1]
                    
                    # Only include high-confidence detections
                    if confidence >= confidence_threshold:
                        text_lines.append(text)
                elif len(result) >= 2:
                    # Fallback if confidence not provided
                    text_lines.append(result[1])
            
            text = '\n'.join(text_lines)
            text = self.clean_ocr_text(text)
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"EasyOCR failed: {e}")
    
    def extract_text(self, image_path, preprocess=True, use_multiple_engines=False):
        """
        Extract text from image using selected OCR engine
        
        Args:
            image_path: Path to image file
            preprocess: Whether to preprocess image (for Tesseract)
            use_multiple_engines: If True, try both engines and return best result
            
        Returns:
            Extracted text string
        """
        results = []
        
        # Try primary engine
        try:
            if self.ocr_engine == 'tesseract':
                text = self.extract_text_tesseract(image_path, preprocess)
                results.append(('tesseract', text))
            elif self.ocr_engine == 'easyocr':
                text = self.extract_text_easyocr(image_path)
                results.append(('easyocr', text))
        except Exception as e:
            print(f"Primary OCR engine ({self.ocr_engine}) failed: {e}")
        
        # Try alternate engine if requested and available
        if use_multiple_engines:
            try:
                if self.ocr_engine == 'tesseract' and EASYOCR_AVAILABLE:
                    # Initialize EasyOCR if not already done
                    if self.easyocr_reader is None:
                        self.easyocr_reader = easyocr.Reader(['en'], gpu=False)
                    text = self.extract_text_easyocr(image_path)
                    results.append(('easyocr', text))
                elif self.ocr_engine == 'easyocr' and OCR_AVAILABLE:
                    text = self.extract_text_tesseract(image_path, preprocess)
                    results.append(('tesseract', text))
            except Exception as e:
                print(f"Alternate OCR engine failed: {e}")
        
        # Return the longest (most complete) result
        if results:
            results.sort(key=lambda x: len(x[1]), reverse=True)
            best_engine, best_text = results[0]
            print(f"Using text from {best_engine} (length: {len(best_text)})")
            return best_text
        else:
            raise Exception("All OCR engines failed")


def extract_text_from_image(image_path, ocr_engine='tesseract'):
    """
    Convenience function to extract text from image
    
    Args:
        image_path: Path to image file
        ocr_engine: 'tesseract' or 'easyocr'
        
    Returns:
        Extracted text string
    """
    ocr = ImageOCR(ocr_engine=ocr_engine)
    return ocr.extract_text(image_path)


if __name__ == '__main__':
    # Test OCR
    if len(sys.argv) < 2:
        print("Usage: python image_ocr.py <image_path> [tesseract|easyocr]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    engine = sys.argv[2] if len(sys.argv) > 2 else 'tesseract'
    
    if not os.path.exists(image_path):
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    
    try:
        ocr = ImageOCR(ocr_engine=engine)
        text = ocr.extract_text(image_path)
        
        print("="*70)
        print("EXTRACTED TEXT FROM IMAGE")
        print("="*70)
        print(f"\nImage: {image_path}")
        print(f"OCR Engine: {engine}")
        print(f"\nExtracted Text:\n{text}")
        print(f"\nText Length: {len(text)} characters")
        print(f"Words: {len(text.split())}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
