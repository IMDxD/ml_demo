import os
import logging

from flask import Flask, render_template, request, send_file

from stylize import stylize_image


app = Flask(__name__)
STYLE_MODEL_PATH = "styles"
logger = logging.getLogger("styling")
logger.setLevel(logging.INFO)
formater = logging.Formatter('%(levelname)s: [%(asctime)s] %(message)s')
main_handler = logging.FileHandler("logs.log")
main_handler.setFormatter(formater)
logger.addHandler(main_handler)

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
    logger.info("Got file")
    img = stylize_image(file.filename, style)
    os.remove(file.filename)
    img.save("tmp.jpg")
    return send_file("tmp.jpg", attachment_filename="styled.jpg")
