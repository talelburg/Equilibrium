import pathlib
import socket

import mongomock
import pytest

from equilibrium.utils.sample import SampleHandler


@pytest.fixture
def resources():
    return pathlib.Path(__file__).absolute().parent / "resources"


@pytest.fixture
def parsing(resources):
    return SampleHandler.parse(str(resources / "small.mind.gz"))


@pytest.fixture
def parsed(parsing):
    return SampleHandler.data_to_full_json(".gz", {
        "user_information": next(parsing),
        "snapshot": next(parsing),
    })


@pytest.fixture(autouse=True, scope="session")
def mongodb():
    with mongomock.patch(servers="127.0.0.1"):
        yield


@pytest.fixture
def simulate_tcp_27017():
    s = socket.socket()
    s.bind(("127.0.0.1", 27017))
    s.listen()
    yield
    s.close()
