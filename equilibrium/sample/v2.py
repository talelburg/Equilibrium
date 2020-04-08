import gzip
import json
import pathlib

from construct import Int32ul
from google.protobuf.json_format import MessageToJson

from equilibrium.equilibrium_pb2 import User, Snapshot


class Adapter:
    def parse(self, path):
        with gzip.GzipFile(path, "rb") as f:
            user_length = Int32ul.parse(f.read(4))
            user = User()
            user.ParseFromString(f.read(user_length))
            yield user
            while True:
                snapshot_length = f.read(4)
                if not snapshot_length:
                    break
                snapshot_length = Int32ul.parse(snapshot_length)
                snapshot = Snapshot()
                snapshot.ParseFromString(f.read(snapshot_length))
                yield snapshot

    def build_dict(self, d):
        return {
            "user_information": d["user_information"].SerializeToString(),
            "snapshot": d["snapshot"].SerializeToString()
        }

    def recover_dict(self, d):
        user_info = User()
        user_info.ParseFromString(d["user_information"])
        snapshot = Snapshot()
        snapshot.ParseFromString(d["snapshot"])
        return {"user_information": user_info, "snapshot": snapshot}

    def build_message(self, user_info, snapshot, path):
        """
        Build a message, intended to be published to a message-queue, with provided user information and snapshot.

        Large fields are saved to disk at the provided path to avoid large messages.

        :param user_info: The user information.
        :param snapshot: The snapshot.
        :param path: The path to save large files at.
        :return: The constructed message.
        """
        color_image_path = pathlib.Path(path) / "color_image.bin"
        color_image_path.write_bytes(snapshot.color_image.data)
        snapshot.color_image.ClearField('data')
        depth_image_path = pathlib.Path(path) / "depth_image.bin"
        depth_image_path.write_text(json.dumps(list(snapshot.depth_image.data)))
        snapshot.depth_image.ClearField('data')
        return json.dumps({
            "user_information": MessageToJson(user_info),
            "snapshot": MessageToJson(snapshot)
        })
