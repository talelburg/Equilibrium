import base64
import datetime
import inspect
import json
import pathlib

import flask
from PIL import Image
from matplotlib import pyplot


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
