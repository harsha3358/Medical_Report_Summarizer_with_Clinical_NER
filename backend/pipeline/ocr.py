import cv2
import pytesseract
from backend.utils.config import ocr_reader

def extract_text(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Invalid image")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    t_text = pytesseract.image_to_string(gray)
    e_text = " ".join(ocr_reader.readtext(gray, detail=0))

    return e_text if len(e_text.split()) > len(t_text.split()) else t_text