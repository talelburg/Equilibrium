import base64
import datetime
import pathlib

import pymongo
import pytest

from equilibrium.api.api import get_app
from equilibrium.api.__main__ import main

USER = {
    "user_id": 1,
    "username": "John Smith",
    "birthday": int(datetime.datetime(year=1997, month=8, day=18).timestamp()),
    "gender": 0,
}

SNAPSHOT = {
    "user_id": 1,
    "timestamp": int(datetime.datetime.now().timestamp() * 1000),
    "feelings": {
        "hunger": 0,
        "thirst": 0,
        "exhaustion": 0,
        "happiness": 0,
    },
    "color_image": {
        "width": 1920,
        "height": 1080,
        "data": str(pathlib.Path(__file__).absolute().parent / "resources/color_image.jpg"),
    }
}

DATA = base64.b64encode(pathlib.Path(SNAPSHOT["color_image"]["data"]).read_bytes()).decode()


@pytest.fixture(scope="module")
def api_state(mongodb, simulate_tcp_27017):
    c = pymongo.MongoClient(host="127.0.0.1", port=27017)
    c.db.users.insert_one(USER)
    c.db.snapshots.insert_one(SNAPSHOT)

    app = get_app("mongodb://127.0.0.1:27017")
    with app.test_client() as client:
        yield client


def test_get_users(api_state):
    r = api_state.get("/users")
    assert r.json == [{"user_id": USER["user_id"], "username": USER["username"]}]


def test_get_user(api_state):
    r = api_state.get(f"/users/{USER['user_id']}")
    assert r.json == {"user_id": USER["user_id"], "username": USER["username"],
                      "birthday": USER["birthday"], "gender": USER["gender"]}


def test_get_snapshots(api_state):
    r = api_state.get(f"/users/{USER['user_id']}/snapshots")
    assert r.json == [SNAPSHOT["timestamp"]]


def test_get_snapshot(api_state):
    r = api_state.get(f"/users/{USER['user_id']}/snapshots/{SNAPSHOT['timestamp']}")
    assert r.json == {"timestamp": SNAPSHOT["timestamp"],
                      "results": ["feelings", "color_image"]}


def test_get_result(api_state):
    r = api_state.get(f"/users/{USER['user_id']}/snapshots/{SNAPSHOT['timestamp']}/feelings")
    assert r.json == SNAPSHOT["feelings"]


def test_get_result_data(api_state):
    r = api_state.get(f"/users/{USER['user_id']}/snapshots/{SNAPSHOT['timestamp']}/color_image/data")
    assert r.json == {"width": SNAPSHOT["color_image"]["width"],
                      "height": SNAPSHOT["color_image"]["height"],
                      "data": DATA
                      }
