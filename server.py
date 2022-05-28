from flask import Flask, request, jsonify
from flask_cors import CORS
from util import get_estimated_price, get_location_names, load_saved_artifacts

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def none():
    return "House Price Predictor API"


@app.route("/hello")
def hello():
    return "Hi"


@app.route("/get_location_namess")
def get_location_namess():
    response = jsonify({"locations": get_location_names()})

    return response


@app.route("/predict_home_price", methods=["POST"])
def predict_home_price():
    location = request.form["location"]
    total_sqft = float(request.form["total_sqft"])
    bhk = int(request.form["bhk"])
    bath = int(request.form["bath"])

    response = jsonify(
        {"estimated_price": get_estimated_price(location, total_sqft, bhk, bath)}
    )

    return response


if __name__ == "__main__":
    print("Starting python flask server")
    load_saved_artifacts()
    app.run()
