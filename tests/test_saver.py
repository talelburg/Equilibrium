import json

import pymongo
from click.testing import CliRunner

from equilibrium.saver import Saver
from equilibrium.saver.__main__ import main


def test_api(parsed, simulate_tcp_27017):
    saver = Saver("mongodb://127.0.0.1:27017")
    parsed["result"] = {"test_api": "test_api"}
    saver.save("test_api", json.dumps(parsed))
    check_results("test_api")


def test_cli(parsed, simulate_tcp_27017, tmp_path):
    parsed["result"] = {"test_cli": "test_cli"}
    p = tmp_path / "f.json"
    with open(p, "w") as f:
        json.dump(parsed, f)
    CliRunner().invoke(main, ["save", "-d", "mongodb://127.0.0.1:27017", "test_cli", str(p)])
    check_results("test_cli")


def check_results(key):
    c = pymongo.MongoClient(host="127.0.0.1", port=27017)
    assert c.db.users.find_one({"user_id": 42})
    assert c.db.snapshots.find_one({"user_id": 42})[key] == key
