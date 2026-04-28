import cv2

def preprocess_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, None, fx=2, fy=2)
    _, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return img