import http.client

from flask import Flask

from app.calc import Calculator
from app.util import Util

app = Flask(__name__)

CALCULATOR = Calculator()
HEADERS = {"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"}


@app.route("/", methods=["GET"])
def hello():
    return "Hello from The Calculator!\n"


@app.route("/calc/add/<op_1>/<op_2>", methods=["GET"])
def add(op_1, op_2):
    try:
        num_1, num_2 = Util.convert_to_number(op_1), Util.convert_to_number(op_2)
        return "{}".format(CALCULATOR.add(num_1, num_2)), http.client.OK, HEADERS
    except TypeError as e:
        return str(e), http.client.BAD_REQUEST, HEADERS


@app.route("/calc/substract/<op_1>/<op_2>", methods=["GET"])
def substract(op_1, op_2):
    try:
        num_1, num_2 = Util.convert_to_number(op_1), Util.convert_to_number(op_2)
        return "{}".format(CALCULATOR.substract(num_1, num_2)), http.client.OK, HEADERS
    except TypeError as e:
        return str(e), http.client.BAD_REQUEST, HEADERS


if __name__ == "__main__":
    app.run(debug=True)