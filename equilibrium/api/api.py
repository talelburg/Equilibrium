import base64
import pathlib

import flask
from flask import jsonify

from equilibrium.utils.database import DatabaseHandler

app = flask.Flask(__name__)


@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(app.config["db"].get_users())


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    return jsonify(app.config["db"].get_user(user_id))


@app.route("/users/<user_id>/snapshots", methods=["GET"])
def get_snapshots(user_id):
    return jsonify(app.config["db"].get_snapshots(user_id))


@app.route("/users/<user_id>/snapshots/<timestamp>", methods=["GET"])
def get_snapshot(user_id, timestamp):
    return jsonify(app.config["db"].get_snapshot(user_id, timestamp))


@app.route("/users/<user_id>/snapshots/<timestamp>/<result_name>", methods=["GET"])
def get_result(user_id, timestamp, result_name):
    result = app.config["db"].get_result(user_id, timestamp, result_name)
    data_path = pathlib.Path(result["data"])
    if data_path.exists():
        result["data"] = f"/users/{user_id}/snapshots/{timestamp}/{result_name}/data"
    return jsonify(result)


@app.route("/users/<user_id>/snapshots/<timestamp>/<result_name>/data", methods=["GET"])
def get_result_data(user_id, timestamp, result_name):
    result = app.config["db"].get_result(user_id, timestamp, result_name)
    data_path = pathlib.Path(result["data"])
    if data_path.exists():
        result["data"] = str(base64.b64encode(data_path.read_bytes()))
    return jsonify(result)


def run_api_server(host, port, database_url):
    app.config["db"] = DatabaseHandler(database_url)
    app.run(host=host, port=port, threaded=True)
