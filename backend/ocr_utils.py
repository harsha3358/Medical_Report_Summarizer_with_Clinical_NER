import cv2
import numpy as np

def preprocess_image(path: str) -> np.ndarray:
    """
    Pre-process an image for OCR:
    1. Load as grayscale
    2. Upscale 2× (improves OCR on low-res scans)
    3. Apply Otsu binarization (adaptive threshold → cleaner text)
    4. Denoise (median blur)
    Returns a NumPy array ready for pytesseract.image_to_string().
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")

    # Upscale 2×
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Denoise before thresholding
    img = cv2.medianBlur(img, 3)

    # Otsu binarization (better than fixed threshold for varied scan quality)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return img