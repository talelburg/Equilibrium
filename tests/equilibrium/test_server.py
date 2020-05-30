import multiprocessing

import pytest
import requests

from equilibrium.server import run_server

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8000
SERVER_ADDRESS = f"http://{SERVER_HOST}:{SERVER_PORT}"


@pytest.fixture
def server_api(tmp_path):
    def publish(message):
        with open(tmp_path / "f.txt", "w") as f:
            f.write(message)

    p = multiprocessing.Process(target=run_server, args=(SERVER_HOST, SERVER_PORT, publish))
    p.start()
    yield
    p.terminate()


def test_api(server_api, parsed):
    r = requests.post(SERVER_ADDRESS + "/snapshot", json=parsed)
    print(r)
