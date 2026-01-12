import easyocr
import cv2
import os

reader = easyocr.Reader(['en'])
def extract_plate(image_path):
    if not os.path.exists(image_path): return None
    try:
        img = cv2.imread(image_path)
        results = reader.readtext(img)
        noise_words = {"NEWYORK", "EMPIRESTATE", "EXCELSIOR", "UHAUL", "PENNSYLVANIA", "NEWJERSEY", "ONTARIO", "GARDENSTATE"}
        candidates = []

        for (_, text, prob) in results:
            clean_text = "".join(e for e in text if e.isalnum()).upper()
            if clean_text in noise_words: continue
            if 6 <= len(clean_text) <= 8: return clean_text
            if len(clean_text) >= 4: candidates.append((clean_text, prob))
        if candidates: return max(candidates, key=lambda x: x[1])[0]
        return None
    except: return None