import base64
from typing import Tuple

import requests

from .equilibrium_pb2 import Snapshot
from .sample import SampleReader


def upload_sample(address: Tuple[str, int], sample_path: str):
    """
    Upload a user's sample to a server.

    :param address: The address of the server.
    :param sample_path: Path of the sample file to be read.
    """
    sample = SampleReader(2).parse(sample_path)
    base_url = f"http://{address[0]}:{address[1]}"
    config = requests.get(base_url + "/config").json()
    for snapshot in sample.snapshots:
        supported_snapshot = Snapshot()
        supported_snapshot.datetime = snapshot.datetime
        for field in config:
            getattr(supported_snapshot, field).ParseFromString(getattr(snapshot, field).SerializeToString())
        requests.post(base_url + "/snapshot", json={
            "user_information": base64.b64encode(sample.user.SerializeToString()).decode('utf-8'),
            "snapshot": base64.b64encode(supported_snapshot.SerializeToString()).decode('utf-8'),
        })



