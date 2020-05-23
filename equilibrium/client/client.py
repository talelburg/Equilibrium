import os

import requests

from equilibrium.utils.sample import SampleHandler


def upload_sample(host: str, port: int, path: str):
    """
    Upload a user's sample to a server.

    :param host: IP address of the server to upload to.
    :param port: Port to be used in communication with server.
    :param path: Path of the sample file to be read.
    """
    base_url = f"http://{host}:{port}"
    parsing = SampleHandler.parse(path)
    _, sample_format = os.path.splitext(path)
    user_info = next(parsing)
    for snapshot in parsing:
        full_json = SampleHandler.data_to_full_json(sample_format, {
            "user_information": user_info,
            "snapshot": snapshot
        })
        requests.post(base_url + "/snapshot", json=full_json)
