import json

import pytest
from click.testing import CliRunner

from equilibrium.cli.__main__ import main

PARAMS = [
    ("users", ["get-users"]),
    ("users/3", ["get-user", "3"]),
    ("users/3/snapshots", ["get-snapshots", "3"]),
    ("users/3/snapshots/17", ["get-snapshot", "3", "17"]),
    ("users/3/snapshots/17/pose", ["get-result", "3", "17", "pose"]),
]
MOCK_DATA = {"key": "value"}
DEFAULT_ADDR = "127.0.0.1:5000"
HOST = "1.1.1.1"
PORT = 1337
ADDR = f"{HOST}:{PORT}"


@pytest.mark.parametrize("url_path, cli_args", PARAMS)
def test_cli(url_path, cli_args, requests_mock):
    requests_mock.get(f"http://{DEFAULT_ADDR}/{url_path}", json=MOCK_DATA)
    result = CliRunner().invoke(main, cli_args).output
    assert json.loads(result.replace("'", '"')) == MOCK_DATA


@pytest.mark.parametrize("url_path, cli_args", PARAMS)
def test_cli_options(url_path, cli_args, requests_mock):
    args = cli_args + ["-h", HOST, "-p", PORT]
    requests_mock.get(f"http://{ADDR}/{url_path}", json=MOCK_DATA)
    result = CliRunner().invoke(main, args).output
    assert json.loads(result.replace("'", '"')) == MOCK_DATA


def test_cli_save_result(requests_mock):
    url_path, cli_args = PARAMS[-1]
    output_filename = "out.txt"
    args = cli_args + ["-s", output_filename]
    requests_mock.get(f"http://{DEFAULT_ADDR}/{url_path}", json=MOCK_DATA)
    r = CliRunner()
    with r.isolated_filesystem():
        r.invoke(main, args, catch_exceptions=False)
        with open(output_filename, "r") as f:
            assert json.load(f) == MOCK_DATA
