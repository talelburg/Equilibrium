import bson
import requests

from equilibrium.sample import SampleHandler


def upload_sample(host: str, port: int, path: str):
    """
    Upload a user's sample to a server.

    :param host: IP address of the server to upload to.
    :param port: Port to be used in communication with server.
    :param path: Path of the sample file to be read.
    """
    base_url = f"http://{host}:{port}"
    handler = SampleHandler(2)
    parsing = handler.parse(path)
    user_info = next(parsing)
    config = requests.get(base_url + "/config").json()
    for snapshot in parsing:
        supported_snapshot = handler.limit_snapshot_fields(snapshot, config)
        requests.post(base_url + "/snapshot", data=bson.dumps(handler.build_dict(user_info, supported_snapshot)))
