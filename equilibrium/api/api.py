import base64
import pathlib

import flask
from flask import jsonify
from flask_cors import CORS

from equilibrium.utils.database import DatabaseHandler

app = flask.Flask(__name__)
CORS(app)

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(app.config["db"].get_users())


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user_id = int(user_id)
    return jsonify(app.config["db"].get_user(user_id))


@app.route("/users/<user_id>/snapshots", methods=["GET"])
def get_snapshots(user_id):
    user_id = int(user_id)
    return jsonify(app.config["db"].get_snapshots(user_id))


@app.route("/users/<user_id>/snapshots/<timestamp>", methods=["GET"])
def get_snapshot(user_id, timestamp):
    user_id = int(user_id)
    timestamp = int(timestamp)
    return jsonify(app.config["db"].get_snapshot(user_id, timestamp))


@app.route("/users/<user_id>/snapshots/<timestamp>/<result_name>", methods=["GET"])
def get_result(user_id, timestamp, result_name):
    user_id = int(user_id)
    timestamp = int(timestamp)
    result = app.config["db"].get_result(user_id, timestamp, result_name)
    if "data" in result and pathlib.Path(result["data"]).exists():
        result["data"] = f"users/{user_id}/snapshots/{timestamp}/{result_name}/data"
    return jsonify(result)


@app.route("/users/<user_id>/snapshots/<timestamp>/<result_name>/data", methods=["GET"])
def get_result_data(user_id, timestamp, result_name):
    user_id = int(user_id)
    timestamp = int(timestamp)
    result = app.config["db"].get_result(user_id, timestamp, result_name)
    if "data" in result and (data_path := pathlib.Path(result["data"])).exists():
        result["data"] = base64.b64encode(data_path.read_bytes()).decode()
    return jsonify(result)


def run_api_server(host, port, database_url):
    app.config["db"] = DatabaseHandler(database_url)
    app.run(host=host, port=port, threaded=True)
