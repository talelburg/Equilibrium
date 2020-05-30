import json

import pytest

from equilibrium.server.server import get_app
from equilibrium.utils.sample import SampleHandler

EXPECTED = {'sample_format': '.gz',
            'user_information': '{\n  "userId": "42",\n  "username": "Dan Gittik",\n  "birthday": 699746400\n}',
            'snapshot': '{\n  "datetime": "1575446887339",\n  "pose": {\n    "translation": {\n      "x": 0.4873843491077423,\n      "y": 0.007090016733855009,\n      "z": -1.1306129693984985\n    },\n    "rotation": {\n      "x": -0.10888676356214629,\n      "y": -0.26755994585035286,\n      "z": -0.021271118915446748,\n      "w": 0.9571326384559261\n    }\n  },\n  "colorImage": {\n    "width": 1920,\n    "height": 1080\n  },\n  "depthImage": {\n    "width": 224,\n    "height": 172\n  },\n  "feelings": {}\n}'}


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
