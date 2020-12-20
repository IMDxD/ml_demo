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
    logger.info(f"Got file {file.filename} and style {style}")
    img = stylize_image(file.filename, style)
    os.remove(file.filename)
    img.save("tmp.jpg")
    return send_file("tmp.jpg", attachment_filename="stylized.jpg")

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


# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)
