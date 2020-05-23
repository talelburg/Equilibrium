import gzip
import json
import pathlib
import struct

from google.protobuf.json_format import MessageToJson, Parse

from equilibrium.equilibrium_pb2 import User, Snapshot
from equilibrium.utils.general.shared_data_storage import get_snapshot_data_dir


class GzipAdapter:
    SAMPLE_FORMAT = ".gz"

    @staticmethod
    def parse(path):
        with gzip.GzipFile(path, "rb") as f:
            user_length, = struct.unpack("<I", f.read(4))
            user = User()
            user.ParseFromString(f.read(user_length))
            yield user
            while True:
                snapshot_length = f.read(4)
                if not snapshot_length:
                    break
                snapshot_length, = struct.unpack("<I", snapshot_length)
                snapshot = Snapshot()
                snapshot.ParseFromString(f.read(snapshot_length))
                yield snapshot

    @staticmethod
    def data_to_full_json(data):
        return {
            "sample_format": GzipAdapter.SAMPLE_FORMAT,
            "user_information": MessageToJson(data["user_information"]),
            "snapshot": MessageToJson(data["snapshot"])
        }

    @staticmethod
    def data_to_light_json(data):
        data_dir_path = get_snapshot_data_dir(data)
        data_dir_path.mkdir(parents=True, exist_ok=True)
        snapshot = data["snapshot"]
        color_image_path = pathlib.Path(data_dir_path) / "color_image.bin"
        color_image_path.write_bytes(snapshot.color_image.data)
        snapshot.color_image.ClearField('data')
        depth_image_path = pathlib.Path(data_dir_path) / "depth_image.bin"
        depth_image_path.write_text(json.dumps(list(snapshot.depth_image.data)))
        snapshot.depth_image.ClearField('data')
        return {
            "sample_format": GzipAdapter.SAMPLE_FORMAT,
            "user_information": MessageToJson(data["user_information"]),
            "snapshot": MessageToJson(snapshot)
        }

    @staticmethod
    def json_to_data(json_dict):
        data = {
            "sample_format": GzipAdapter.SAMPLE_FORMAT,
            "user_information": Parse(json_dict["user_information"], User()),
            "snapshot": Parse(json_dict["snapshot"], Snapshot())
        }
        return data
