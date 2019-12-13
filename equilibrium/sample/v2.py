import gzip

from construct import Int32ul

from equilibrium.equilibrium_pb2 import User, Snapshot


class Adapter:
    def parse(self, path):
        with gzip.GzipFile(path, "rb") as f:
            user_length = Int32ul.parse(f.read(4))
            user = User()
            user.ParseFromString(f.read(user_length))
            snapshots = []
            while True:
                snapshot_length = f.read(4)
                if not snapshot_length:
                    break
                snapshot_length = Int32ul.parse(snapshot_length)
                snapshots.append(Snapshot())
                snapshots[-1].ParseFromString(f.read(snapshot_length))
            return Version2Sample(user, snapshots)

    def build(self, obj):
        data = b""
        user_message = obj.user.SerializeToString()
        data += Int32ul.build(len(user_message))
        data += user_message
        for snapshot in obj.snapshots:
            snapshot_message = snapshot.SerializeToString()
            data += Int32ul.build(len(snapshot_message))
            data += snapshot_message
        return data


class Version2Sample:
    def __init__(self, user, snapshots):
        self.user = user
        self.snapshots = snapshots

    def __str__(self):
        print(f"Sample v2: user={self.user}, snapshots={self.snapshots}")
