import json

import pytest

from equilibrium.server.server import get_app
from equilibrium.server.__main__ import main
from equilibrium.utils.sample import SampleHandler


@pytest.fixture
def server_api(tmp_path):
    p = tmp_path / "f.txt"

    def publish(message):
        with open(p, "w") as f:
            f.write(message)

    app = get_app(publish)
    with app.test_client() as client:
        yield client, p


def test_api(server_api, parsed):
    client, data = server_api
    client.post("/snapshot", json=parsed)

    with open(data, "r") as f:
        result = json.load(f)

    parsed_data = SampleHandler.json_to_data(parsed)
    result_data = SampleHandler.json_to_data(result)
    assert parsed_data["user_information"] == result_data["user_information"]
    assert parsed_data["snapshot"].datetime == result_data["snapshot"].datetime
    assert parsed_data["snapshot"].pose == result_data["snapshot"].pose
    assert parsed_data["snapshot"].feelings == result_data["snapshot"].feelings
    assert parsed_data["snapshot"].color_image.width == result_data["snapshot"].color_image.width
    assert parsed_data["snapshot"].color_image.height == result_data["snapshot"].color_image.height
    assert parsed_data["snapshot"].depth_image.width == result_data["snapshot"].depth_image.width
    assert parsed_data["snapshot"].depth_image.height == result_data["snapshot"].depth_image.height
