import gzip

from construct import Int32ul

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

    def build_dict(self, user_info, snapshot):
        return {
            "user_information": user_info.SerializeToString(),
            "snapshot": snapshot.SerializeToString()
        }

    def limit(self, snapshot, fields):
        supported_snapshot = Snapshot()
        supported_snapshot.datetime = snapshot.datetime
        for field in fields:
            getattr(supported_snapshot, field).ParseFromString(getattr(snapshot, field).SerializeToString())
        return supported_snapshot
