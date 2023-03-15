from flask import Flask, request
import logging
from platereaderweb import PlateReaderWeb

app = Flask(__name__)
plate_reader = PlateReaderWeb(url="http://51.250.83.169:7878/images/")


@app.route("/")
def hello():
    return "<h1><center>Hello!</center></h1>"


@app.route("/readNumber/<image_name>")
def readnumber(image_name):
    number = plate_reader.predict(image_name)
    if isinstance(number, dict):
        return f"Error while fetching image {image_name}.", number["error"]
    return {"number": number}


@app.route("/readNumbers", methods=["POST"])
# {"images": ["000", "0091"]} -> {"numbers": [...]}
def readnumbers():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        if "images" not in request.json or not isinstance(request.json["images"], list):
            return 'Bad json. Use "{"images": ["000", "0091", ...]} scheme.', 400
        res = []
        for image_name in request.json["images"]:
            if image_name.isalnum():
                number = plate_reader.predict(image_name)
                if isinstance(number, dict):
                    return f"Error while fetching image {image_name}.", number["error"]
                res.append(plate_reader.predict(image_name))
            else:
                return "Only alfanumeric names are supported!", 400
        return {"numbers": res}
    else:
        return "Content type is not supported.", 400


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.run(host='0.0.0.0', port=8080, debug=True)
