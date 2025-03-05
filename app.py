from flask import Flask, request, render_template, send_file
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set Tesseract path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route("/", methods=["GET", "POST"])
def index():
    final_image_path = None
    if request.method == "POST":
        if "clothing" not in request.files or "label" not in request.files:
            return "Missing file(s)", 400
        
        clothing_file = request.files["clothing"]
        label_file = request.files["label"]
        
        clothing_image = Image.open(clothing_file)
        label_image = Image.open(label_file)
        
        # Extract text from label
        extracted_text = pytesseract.image_to_string(label_image)
        
        # Overlay text on clothing image
        draw = ImageDraw.Draw(clothing_image)
        font = ImageFont.load_default()
        draw.text((10, 10), extracted_text, fill=(255, 255, 255), font=font)
        
        # Save final image
        final_image_path = os.path.join(UPLOAD_FOLDER, "final_image.png")
        clothing_image.save(final_image_path)
    
    return render_template("index.html", final_image=final_image_path)

@app.route("/download")
def download():
    return send_file("static/uploads/final_image.png", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)