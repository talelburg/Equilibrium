import bson
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
    handler = SampleHandler("gzip_protobuf")
    parsing = handler.parse(path)
    user_info = next(parsing)
    for snapshot in parsing:
        bsonable = handler.data_to_dict({
            "user_information": user_info,
            "snapshot": snapshot
        })
        requests.post(base_url + "/snapshot", data=bson.dumps(bsonable))
