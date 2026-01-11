from flask import Flask, render_template, request
from ocr import extract_text, speak_text
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
INBUILT_FOLDER = "inbuilt_forms"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    inbuilt_forms = os.listdir(INBUILT_FOLDER)

    if request.method == "POST":
        language = request.form.get("language")

        # Inbuilt form
        selected_form = request.form.get("inbuilt_form")
        if selected_form:
            path = os.path.join(INBUILT_FOLDER, selected_form)
            text = extract_text(path)
            speak_text(text, language)

        # Uploaded image
        elif "image" in request.files and request.files["image"].filename != "":
            file = request.files["image"]
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            text = extract_text(path)
            speak_text(text, language)

        # Camera image
        elif "camera_image" in request.files:
            file = request.files["camera_image"]
            path = os.path.join(UPLOAD_FOLDER, "camera.jpg")
            file.save(path)
            text = extract_text(path)
            speak_text(text, language)

    return render_template("index.html", text=text, inbuilt_forms=inbuilt_forms)

if __name__ == "__main__":
    app.run(debug=True)
