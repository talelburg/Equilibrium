import bson
import flask
from flask import request

from equilibrium import SampleHandler

app = flask.Flask(__name__)


@app.route("/snapshot", methods=["POST"])
def post_snapshot():
    data = request.data
    bsonable = bson.loads(data)
    data = SampleHandler(2).recover_dict(bsonable)
    app.config["publish"](data)
    return ""


def run_server(host, port, publish):
    app.config["publish"] = publish
    app.run(host=host, port=port, threaded=True)
