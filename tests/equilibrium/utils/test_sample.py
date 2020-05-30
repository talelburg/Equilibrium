import json

import pytest


@pytest.fixture
def color_image_data(resources):
    return (resources / "color_image.bin").read_bytes()


@pytest.fixture
def depth_image_data(resources):
    with open(resources / "depth_image.bin", "r") as f:
        return json.load(f)


def test_parse_user(parsing):
    user = next(parsing)
    assert user.user_id == 42
    assert user.username == "Dan Gittik"
    assert user.birthday == 699746400
    assert user.gender == 0


def test_parse_snapshot(parsing, color_image_data, depth_image_data):
    user = next(parsing)
    snapshot = next(parsing)
    assert snapshot.datetime == 1575446887339
    pose = snapshot.pose
    translation = pose.translation
    assert translation.x == 0.4873843491077423
    assert translation.y == 0.007090016733855009
    assert translation.z == -1.1306129693984985
    rotation = pose.rotation
    assert rotation.x == -0.10888676356214629
    assert rotation.y == -0.26755994585035286
    assert rotation.z == -0.021271118915446748
    assert rotation.w == 0.9571326384559261
    feelings = snapshot.feelings
    assert feelings.hunger == 0
    assert feelings.thirst == 0
    assert feelings.exhaustion == 0
    assert feelings.happiness == 0
    color_image = snapshot.color_image
    assert color_image.height == 1080
    assert color_image.width == 1920
    assert color_image.data == color_image_data
    depth_image = snapshot.depth_image
    assert depth_image.height == 172
    assert depth_image.width == 224
    assert list(depth_image.data) == depth_image_data
