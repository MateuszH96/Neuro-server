from flask import Flask, jsonify, send_file
import json
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world"

@app.route("/tricks")
def return_data():
    try:
        with open('tricks.json') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

@app.route("/image/<image_name>")
def get_image(image_name):
    image_path = os.path.join('images', image_name)
    if os.path.exists(image_path):
        # Open an image file
        with Image.open(image_path) as img:
            # Resize the image to 800x600
            img = img.resize((800, 600), Image.ANTIALIAS)

            # Save it to a BytesIO object in WebP format
            img_io = BytesIO()
            img.save(img_io, 'WEBP', quality=80)  # Set quality to 80 (out of 100)
            img_io.seek(0)

            return send_file(img_io, mimetype='image/webp')
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
