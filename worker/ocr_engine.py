import easyocr
import cv2
import os

# Initialize the reader
# We use 'en' (English). The models are already downloaded in your container.
reader = easyocr.Reader(['en'])


def extract_plate(image_path):
    """
    Uses EasyOCR to detect and transcribe license plate text with noise filtering.
    """
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None

    try:
        # 1. Read image with OpenCV
        img = cv2.imread(image_path)

        # 2. Run OCR
        # detail=1 returns bounding box and confidence score
        results = reader.readtext(img)

        # 3. Filter and parse results
        for (bbox, text, prob) in results:
            # Clean text: uppercase and alphanumeric only
            clean_text = "".join(e for e in text if e.isalnum()).upper()

            # List of common "noise" strings to ignore
            noise_words = [
                "NEWYORK", "EMPIRESTATE", "EXCELSIOR", "UHAUL",
                "PENNSYLVANIA", "NEWJERSEY", "ONTARIO", "GARDENSTATE"
            ]

            if clean_text in noise_words:
                print(f"Filtering noise: {clean_text}")
                continue

            # License plates are typically 6 to 8 characters long
            if 6 <= len(clean_text) <= 8:
                print(f"OCR Detected Plate: {clean_text} (Confidence: {prob:.2f})")
                return clean_text

        # If no 6-8 char string is found, return the highest confidence result over 4 chars
        if results:
            # Sort by confidence score
            results.sort(key=lambda x: x[2], reverse=True)
            for (bbox, text, prob) in results:
                clean_text = "".join(e for e in text if e.isalnum()).upper()
                if len(clean_text) >= 4:
                    return clean_text

        return None
    except Exception as e:
        print(f"OCR processing failed: {e}")
        return None