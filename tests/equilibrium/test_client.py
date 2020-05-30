import json

import pytest
from click.testing import CliRunner

from equilibrium.client import upload_sample
from equilibrium.client.__main__ import main
from equilibrium.utils.sample import SampleHandler

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_ADDRESS = f"http://{SERVER_HOST}:{SERVER_PORT}"


@pytest.fixture
def requests(requests_mock):
    requests_mock.post(SERVER_ADDRESS + "/snapshot")
    yield requests_mock


def test_api(requests, resources, parsed):
    upload_sample(SERVER_HOST, SERVER_PORT, str(resources / "small.mind.gz"))
    data = json.loads(requests.last_request.body)

    assert data["user_information"] == parsed["user_information"]
    assert data["snapshot"] == parsed["snapshot"]


def test_cli(requests, resources, parsed):
    args = ["-t", "upload-sample", "-h", f"{SERVER_HOST}", "-p", f"{SERVER_PORT}", str(resources / "small.mind.gz")]
    runner = CliRunner()
    runner.invoke(main, args)
    data = json.loads(requests.last_request.body)

    assert data["user_information"] == parsed["user_information"]
    assert data["snapshot"] == parsed["snapshot"]
