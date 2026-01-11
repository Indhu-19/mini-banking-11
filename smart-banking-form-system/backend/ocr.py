import pytesseract
import cv2
import pyttsx3

def extract_text(image_path):
    img = cv2.imread(image_path)

    # Basic preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]

    text = pytesseract.image_to_string(gray)
    return text


def speak_text(text, language="en"):
    engine = pyttsx3.init()

    # Change voice based on language (basic support)
    voices = engine.getProperty('voices')

    if language == "en":
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[0].id)  # can customize later

    engine.say(text)
    engine.runAndWait()
