import os
import logging
import tempfile

from flask import Flask, render_template, request, send_file

from stylize import stylize_image


app = Flask(__name__)
STYLE_MODEL_PATH = "styles"
logger = logging.getLogger("styling")
logger.setLevel(logging.INFO)
formater = logging.Formatter('%(levelname)s: [%(asctime)s] %(message)s')
main_handler = logging.StreamHandler()
main_handler.setFormatter(formater)
logger.addHandler(main_handler)

if not os.path.exists(STYLE_MODEL_PATH):
    os.makedirs(STYLE_MODEL_PATH)


def get_path(file_name):
    return os.path.join(tempfile.gettempdir(), file_name)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/stylize", methods=["POST"])
def stylize():
    style = request.values["style"]
    file = request.files["file"]
    logger.info(f"Got file {file} and style {style}")
    filepath = get_path(file.filename)
    file.save(filepath)
    logger.info(f"File saved to {filepath}")
    img = stylize_image(filepath, style)
    os.remove(filepath)
    savedpath = get_path("tmp.jpg")
    img.save(savedpath)
    logger.info(f"Image saved to {savedpath}")
    return send_file(savedpath, attachment_filename="stylized.jpg")

# @app.route("/stylize/<string:style>", methods=["GET", "POST"])
# def stylize(style):
#     r = request
#     # logger.info(f"In stylize with style {style} and filename {filename}")
#     # file = request.files["file"]
#     # file.save(filename)
#     # logger.info(f"Got file {file.filename} and style {style}")
#     # img = stylize_image(filename, style)
#     # img.save("tmp.jpg")
#     # return style, 200, {'Content-Type': 'text/plain'}
#     return send_file("tmp.jpg", mimetype='image/jpg')
#
#
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
