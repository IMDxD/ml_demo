import os

from flask import Flask, render_template, request, send_file

from stylize import stylize_image


app = Flask(__name__)
STYLE_MODEL_PATH = "styles"

if not os.path.exists(STYLE_MODEL_PATH):
    os.makedirs(STYLE_MODEL_PATH)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stylize", methods=["POST"])
def stylize():
    style = request.values["style"]
    file = request.files["file"]
    file.save(file.filename)
    img = stylize_image(file.filename, style)
    os.remove(file.filename)
    img.save("tmp.jpg")
    return send_file("tmp.jpg", attachment_filename="styled.jpg")
