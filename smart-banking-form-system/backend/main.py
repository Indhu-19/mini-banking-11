import pytesseract
import cv2

def extract_text(image_path):
    img = cv2.imread(image_path)

    # Resize for better OCR
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)

    # Thresholding for clearer text
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR configuration
    custom_config = r'--oem 3 --psm 4'
    text = pytesseract.image_to_string(thresh, config=custom_config)

    return text


def detect_fields(text):
    # Common form field labels
    possible_fields = [
        "full name",
        "name",
        "date of birth",
        "phone",
        "phone number",
        "email",
        "email address",
        "address",
        "residential address",
        "loan type",
        "loan amount",
        "loan amount requested",
        "loan purpose",
        "employer name",
        "job title",
        "monthly income",
        "signature",
        "date"
    ]

    detected = set()

    for line in text.split("\n"):
        line_lower = line.lower().strip()

        for field in possible_fields:
            if field in line_lower:
                detected.add(field.title())

    return sorted(list(detected))


if __name__ == "__main__":
    image_path = "sample_form.jpg"   # change this to any image path

    text = extract_text(image_path)

    print("\nRAW OCR TEXT:\n")
    print(text)

    print("\nDETECTED FORM FIELDS:\n")
    fields = detect_fields(text)

    for f in fields:
        print("-", f)
