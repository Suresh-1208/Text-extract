from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import pytesseract
import re
import os
from PIL import Image
from torchvision import transforms

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)

# Ensure Tesseract OCR is set up correctly
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Update if needed for your system

# Define preprocessing for OCR
def preprocess_image(image):
    """
    Preprocess the image to enhance OCR accuracy.
    """
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply thresholding
    thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)[1]
    return thresh

# Define function to extract invoice details using regex
def extract_invoice_details(text):
    """
    Extract key invoice details using regex patterns.
    """
    patterns = {
        "Invoice Number": r"Invoice Number[:\s]*([A-Za-z0-9-]+)",
        "Date": r"Date[:\s]*([\d{2}/\d{2}/\d{4}]+)",
        "Total Amount": r"Total Amount[:\s]*\$?([\d{1,3}(,\d{3})*(\.\d{2})?]+)"
    }
    extracted = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        extracted[key] = match.group(1) if match else "Not found"
    return extracted

# OCR and invoice extraction endpoint
@app.route('/extract-invoice', methods=['POST'])
def extract_invoice():
    """
    Accept an uploaded image, process it with OCR, and extract invoice details.
    """
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No image file provided."}), 400

        # Get the uploaded image
        image_file = request.files['image']
        image = Image.open(image_file).convert("RGB")
        
        # Convert the image to OpenCV format
        open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Preprocess the image
        processed_image = preprocess_image(open_cv_image)

        # Perform OCR using Tesseract
        extracted_text = pytesseract.image_to_string(processed_image)

        # Extract invoice details
        invoice_details = extract_invoice_details(extracted_text)

        return jsonify({"status": "success", "details": invoice_details, "raw_text": extracted_text})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Health check endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

# Run the Flask app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
