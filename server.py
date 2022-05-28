from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import json
import numpy as np

__data_columns = None
__locations = None
__model = None

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def none():
    return "House Price Predictor API"


@app.route("/hello")
def hello():
    return "Hi"


@app.route("/get_location_names")
def get_location_names():
    with open("columns.json", "r") as f:
        data_columns = json.load(f)["data_columns"]
        locations = data_columns[3:]
    response = jsonify({"locations": locations})

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


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    with open("columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        __locations = __data_columns[3:]

    with open(
        "Bengaluru_House_Data_model.pickle",
        "rb",
    ) as f:
        __model = pickle.load(f)

    print("loading saved artifacts...done")


def get_locations():
    return __locations


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


if __name__ == "__main__":
    print("Starting python flask server")
    load_saved_artifacts()
    app.run()
