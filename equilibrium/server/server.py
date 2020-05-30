import json

import flask
from flask import request

from equilibrium.utils.sample import SampleHandler


def run_server(host, port, publish):
    app = get_app(publish)
    app.run(host=host, port=port, threaded=True)


def get_app(publish):
    app = flask.Flask(__name__)
    app.config["publish"] = publish

    @app.route("/snapshot", methods=["POST"])
    def post_snapshot():
        json_dict = request.json
        data = SampleHandler.json_to_data(json_dict)
        message = json.dumps(SampleHandler.data_to_light_json(json_dict["sample_format"], data))
        app.config["publish"](message)
        return ""

    return app
