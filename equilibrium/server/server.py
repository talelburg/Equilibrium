import bson
import flask
from flask import request

from equilibrium.sample import SampleHandler

app = flask.Flask(__name__)


@app.route("/snapshot", methods=["POST"])
def post_snapshot():
    data = request.data
    bsonable = bson.loads(data)
    data = SampleHandler("gzip_protobuf").dict_to_data(bsonable)
    app.config["publish"](data)
    return ""


def run_server(host, port, publish):
    app.config["publish"] = publish
    app.run(host=host, port=port, threaded=True)
