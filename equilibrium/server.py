import base64
import datetime
import inspect
import json
import pathlib

import flask
from PIL import Image
from matplotlib import pyplot

from equilibrium.equilibrium_pb2 import User, Snapshot

app = flask.Flask(__name__)


@app.route("/config", methods=["GET"])
def get_config():
    return flask.jsonify([k for k in Server.fields])


@app.route("/snapshot", methods=["POST"])
def post_snapshot():
    user_information = User()
    user_information.ParseFromString(base64.b64decode(flask.request.json["user_information"]))
    user_path = app.config['data_path'] / f'{user_information.user_id}'
    if not user_path.exists():
        user_path.mkdir()
    snapshot = Snapshot()
    snapshot.ParseFromString(base64.b64decode(flask.request.json["snapshot"]))
    timestamp = datetime.datetime.fromtimestamp(snapshot.datetime / 1000)
    snapshot_path = user_path / f'{timestamp:%Y-%m-%d_%H-%M-%S-%f}'
    if not snapshot_path.exists():
        snapshot_path.mkdir()
    Server.parse(snapshot_path, snapshot)
    return ""


def run_server(port, data_dir):
    app.config["data_path"] = pathlib.Path(data_dir)
    app.run(port=port, threaded=True)


class Server:
    fields = {}

    @classmethod
    def parses(cls, *field_names):
        """
        Decorator to register parsers for snapshot fields.
        """

        def decorator(obj):
            if inspect.isclass(obj):
                parser = obj().parse
            else:
                parser = obj
            for field_name in field_names:
                cls.fields[field_name] = parser
            return obj

        return decorator

    @classmethod
    def parse(cls, directory: pathlib.Path, snapshot):
        """
        Parse a given snapshot. Calls registered parsers on received arguments.
        """
        for parser in set(cls.fields.values()):
            parser(directory, snapshot)


@Server.parses("pose")
def parse_pose(directory, snapshot):
    data = {
        "translation": {
            "x": snapshot.translation.x,
            "y": snapshot.translation.y,
            "z": snapshot.translation.z,
        },
        "rotation": {
            "x": snapshot.rotation.x,
            "y": snapshot.rotation.y,
            "z": snapshot.rotation.z,
            "w": snapshot.rotation.w,
        },
    }
    with open(directory / "translation.json", "w") as f:
        json.dump(data, f, indent=4)


@Server.parses("color_image")
def parse_color_image(directory, snapshot):
    color_image = snapshot.color_image
    image = Image.new("RGB", (color_image.width, color_image.height))
    image.putdata([tuple(color_image.data[3 * i:3 * i + 3]) for i in range(len(color_image.data) // 3)])
    image.save(str(directory / "color_image.jpg"))


@Server.parses("depth_image")
def parse_depth_image(directory, snapshot):
    depth_image = snapshot.depth_image
    data = [[depth_image.data[i * depth_image.width + j] for j in range(depth_image.width)]
            for i in range(depth_image.height)]
    pyplot.imshow(data).write_png(str(directory / "depth_image.jpg"))


@Server.parses("feelings")
def parse_feelings(directory, snapshot):
    data = {
        "hunger": snapshot.feelings.hunger,
        "thirst": snapshot.feelings.thirst,
        "exhaustion": snapshot.feelings.exhaustion,
        "happiness": snapshot.feelings.happiness,
    }
    with open(directory / "feelings.json", "w") as f:
        json.dump(data, f, indent=4)


@Server.parses("pose", "depth_image")
def parse_location(directory, snapshot):
    pass
