"""
GUI Application for Language Detection
Upload text or image files and detect language with statistics
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except:
        pass


class LanguageDetectionGUI:
    """GUI Application for Language Detection"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multilingual Language Detector")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Check if model exists
        self.model_path = 'multilingual_detector_model.pkl'
        self.detector = None
        self.ocr = None
        
        # Initialize components
        self.load_model()
        self.setup_ui()
    
    def load_model(self):
        """Load the language detection model"""
        if not os.path.exists(self.model_path):
            messagebox.showerror(
                "Model Not Found",
                f"Model file not found: {self.model_path}\n\n"
                "Please train the model first:\n"
                "  python model_trainer.py"
            )
            self.root.destroy()
            return
        
        try:
            from language_detector import LanguageDetector
            self.detector = LanguageDetector(self.model_path)
            print("Model loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {e}")
            self.root.destroy()
            return
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Multilingual Language Detection",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # File input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        # Text file button
        ttk.Button(
            input_frame,
            text="Upload Text File (.txt)",
            command=self.upload_text_file,
            width=20
        ).grid(row=0, column=0, padx=(0, 10), pady=5)
        
        # Image file button
        ttk.Button(
            input_frame,
            text="Upload Image File (.jpg, .png, .jpeg)",
            command=self.upload_image_file,
            width=25
        ).grid(row=0, column=1, padx=(0, 10), pady=5)
        
        # Text input area
        ttk.Label(
            input_frame,
            text="Or enter text directly:"
        ).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.text_input = scrolledtext.ScrolledText(
            input_frame,
            height=8,
            wrap=tk.WORD,
            font=("Arial", 10)
        )
        self.text_input.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.rowconfigure(2, weight=1)
        
        # Process button
        process_button = ttk.Button(
            input_frame,
            text="Detect Language",
            command=self.process_input,
            width=20
        )
        process_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready - Upload a file or enter text")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="5"
        )
        status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Results text area
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear button
        clear_button = ttk.Button(
            main_frame,
            text="Clear All",
            command=self.clear_all
        )
        clear_button.grid(row=4, column=0, pady=(10, 0))
    
    def upload_text_file(self):
        """Upload and load text file"""
        file_path = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.text_input.delete(1.0, tk.END)
                self.text_input.insert(1.0, content)
                self.status_var.set(f"Text file loaded: {os.path.basename(file_path)}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {e}")
    
    def upload_image_file(self):
        """Upload image file and extract text using OCR"""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.status_var.set("Extracting text from image... Please wait...")
            self.root.update()
            
            try:
                # Try to use OCR with multiple engines
                text = self.extract_text_from_image(file_path, use_multiple=True)
                
                if text and len(text.strip()) > 0:
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, text)
                    
                    # Show extracted text preview
                    # Show more detailed status
                    words = len(text.split())
                    preview = text[:80].replace('\n', ' ') + "..." if len(text) > 80 else text.replace('\n', ' ')
                    self.status_var.set(
                        f"✓ Text extracted: {os.path.basename(file_path)} | "
                        f"{len(text)} chars, {words} words | Preview: {preview}"
                    )
                else:
                    messagebox.showwarning(
                        "No Text Found",
                        "Could not extract any text from the image.\n"
                        "Please ensure the image contains readable text."
                    )
                    self.status_var.set("No text extracted from image")
            
            except ImportError as e:
                messagebox.showerror(
                    "OCR Not Available",
                    f"OCR functionality not available:\n{e}\n\n"
                    "Please install OCR dependencies:\n"
                    "  pip install pytesseract pillow opencv-python\n"
                    "Or install EasyOCR:\n"
                    "  pip install easyocr"
                )
                self.status_var.set("OCR not available")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to extract text from image: {e}")
                self.status_var.set("Error extracting text from image")
    
    def extract_text_from_image(self, image_path, use_multiple=False):
        """Extract text from image using OCR"""
        try:
            from image_ocr import ImageOCR
            if self.ocr is None:
                # Try EasyOCR first (doesn't require system installation), fallback to Tesseract
                try:
                    self.ocr = ImageOCR(ocr_engine='easyocr')
                    print("Using EasyOCR for text extraction")
                except Exception as e1:
                    try:
                        self.ocr = ImageOCR(ocr_engine='tesseract')
                        print("Using Tesseract OCR for text extraction")
                    except Exception as e2:
                        error_msg = (
                            "Neither OCR engine is available.\n\n"
                            "Install EasyOCR (recommended):\n"
                            "  python -m pip install easyocr\n\n"
                            "Or install Tesseract OCR:\n"
                            "  python -m pip install pytesseract pillow opencv-python\n"
                            "  And install Tesseract from: https://github.com/tesseract-ocr/tesseract/wiki"
                        )
                        raise ImportError(error_msg) from e1
            
            # Use multiple engines for better accuracy
            text = self.ocr.extract_text(image_path, preprocess=True, use_multiple_engines=use_multiple)
            return text
        
        except ImportError:
            raise
        except Exception as e:
            raise Exception(f"OCR extraction failed: {e}")
    
    def process_input(self):
        """Process the input text and detect language"""
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showwarning("No Input", "Please enter text or upload a file first.")
            return
        
        self.status_var.set("Processing... Please wait...")
        self.root.update()
        
        try:
            # Analyze the text
            result = self.detector.analyze(text, include_probabilities=False)
            
            # Format results
            output = self.format_results(text, result)
            
            # Display results
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, output)
            self.results_text.config(state=tk.DISABLED)
            
            self.status_var.set("Language detected successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect language: {e}")
            self.status_var.set("Error during processing")
    
    def format_results(self, text, result):
        """Format analysis results for display"""
        stats = result['statistics']
        
        output = "=" * 70 + "\n"
        output += "LANGUAGE DETECTION RESULTS\n"
        output += "=" * 70 + "\n\n"
        
        output += f"Detected Language: {result['detected_language']}\n"
        output += f"Confidence: {result['confidence']:.4f} ({result['confidence']*100:.2f}%)\n\n"
        
        output += "-" * 70 + "\n"
        output += "TEXT STATISTICS\n"
        output += "-" * 70 + "\n\n"
        
        output += f"Total Characters: {stats['total_characters']}\n"
        output += f"Characters (no spaces): {stats['characters_no_spaces']}\n"
        output += f"Letters: {stats['letters']}\n"
        output += f"Words: {stats['words']}\n"
        output += f"Spaces: {stats['spaces']}\n"
        output += f"Lines: {stats['lines']}\n\n"
        
        output += "-" * 70 + "\n"
        output += "EXTRACTED TEXT (for verification)\n"
        output += "-" * 70 + "\n"
        
        text_preview = text[:500] + "..." if len(text) > 500 else text
        output += f"\n{text_preview}\n"
        
        if len(text) != len(text_preview):
            output += f"\n[Full text has {len(text)} characters]\n"
        
        return output
    
    def clear_all(self):
        """Clear all input and results"""
        self.text_input.delete(1.0, tk.END)
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Ready - Upload a file or enter text")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = LanguageDetectionGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
