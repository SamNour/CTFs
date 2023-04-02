import os
from flask import Flask, request, send_file

app = Flask(__name__)


@app.route('/image')
def _serve_image():
    requested_image = request.args.get("filename")
    if not requested_image:
        return "No image specified", 404
    image_path = os.path.join(os.getcwd(), requested_image)

    if not os.path.isfile(image_path):
        return "Image not found", 404
    return send_file(image_path)



if __name__ == '__main__':
    app.run(debug=False, port=6000)

