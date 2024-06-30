from flask import Flask, jsonify, send_file
import json
import os
from PIL import Image
from io import BytesIO
from time import gmtime, strftime

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

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
    with open("./statistic.txt", "a") as myfile:
        myfile.write(strftime("%Y-%m-%d %H:%M:%S\n", gmtime()))
    image_path = os.path.join('images', image_name)
    if os.path.exists(image_path):
        # Open an image file
        with Image.open(image_path) as img:
            img = img.resize((1107,620), Image.ANTIALIAS)

            # Save it to a BytesIO object in WebP format
            img_io = BytesIO()
            img.save(img_io, 'WEBP', quality=100)
            img_io.seek(0)

            return send_file(img_io, mimetype='image/webp')
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
