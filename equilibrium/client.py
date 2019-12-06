from typing import Tuple

from .protocol import Hello, Config, Snapshot
from .sample import Sample
from .utils import Connection


def upload_sample(address: Tuple[str, int], sample_path: str):
    """
    Upload a user's thought to a server.

    :param address: The address of the server.
    :param sample_path: Path of the sample file to be read.
    """

    def send_hook(obj, ctx):
        snapshot = obj
        with Connection.connect(*address) as connection:
            hello = Hello.build(ctx.user_information)
            connection.send_message(hello)
            config_message = connection.receive_message()
            config = Config.parse(config_message)
            if "translation" not in config.fields:
                snapshot.translation.x = 0
                snapshot.translation.y = 0
                snapshot.translation.z = 0
            if "rotation" not in config.fields:
                snapshot.rotation.x = 0
                snapshot.rotation.y = 0
                snapshot.rotation.z = 0
                snapshot.rotation.w = 0
            if "color_image" not in config.fields:
                snapshot.color_image.width = 0
                snapshot.color_image.height = 0
                snapshot.color_image.data = []
            if "depth_image" not in config.fields:
                snapshot.depth_image.width = 0
                snapshot.depth_image.height = 0
                snapshot.depth_image.data = []
            if "emotions" not in config.fields:
                snapshot.feelings.hunger = 0
                snapshot.feelings.thirst = 0
                snapshot.feelings.exhaustion = 0
                snapshot.feelings.happiness = 0
            supported_snapshot = Snapshot.build(snapshot)
            connection.send_message(supported_snapshot)

    Sample(send_hook).parse_file(sample_path)
