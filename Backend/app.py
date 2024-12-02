from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
CORS(app)  

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image):
    try:
        
        image = image.resize((image.width * 2, image.height * 2))
        
        image = image.convert("L")
       
        extracted_text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')
        return extracted_text.strip()
    except Exception as e:
        return f"Error during OCR processing: {e}"

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Text Extractor</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            text-align: center;
            background-color: rgba(0, 0, 0, 0.7);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            width: 90%;
        }

        h1 {
            margin-bottom: 20px;
            font-size: 28px;
        }

        form {
            margin-top: 20px;
        }

        label {
            font-size: 18px;
            margin-bottom: 10px;
            display: block;
        }

        input[type="file"] {
            margin: 10px 0;
            font-size: 16px;
        }

        button {
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #45a049;
        }

        button:active {
            transform: scale(0.98);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to the Image Text Extractor</h1>
        <form action="/extract_text" method="post" enctype="multipart/form-data">
            <label for="file">Upload an image:</label>
            <input type="file" id="file" name="file" accept="image/*" required>
            <button type="submit">Extract Text</button>
        </form>
    </div>
</body>
</html>

    """

@app.route('/extract_text', methods=['POST'])
def extract_text():

    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    try:
        image = Image.open(io.BytesIO(file.read()))
        extracted_text = extract_text_from_image(image)
        return jsonify({"extracted_text": extracted_text})
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
