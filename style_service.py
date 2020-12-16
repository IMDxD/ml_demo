import os

from flask import Flask, request, send_file

from stylize import stylize_image


app = Flask(__name__)
STYLE_MODEL_PATH = "styles"

if not os.path.exists(STYLE_MODEL_PATH):
    os.makedirs(STYLE_MODEL_PATH)


@app.route("/<style>", methods=["GET", "POST"])
def stylize(style):
    file = request.files['file']
    file.save(file.filename)
    img = stylize_image(file.filename, style)
    os.remove(file.filename)
    img.save("tmp.jpg")
    return send_file("tmp.jpg", attachment_filename="styled.jpg")


app.run("127.0.0.1", 5000)
