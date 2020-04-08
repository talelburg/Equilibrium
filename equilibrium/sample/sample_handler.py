from equilibrium.sample import v2


class SampleHandler:
    adapters = {2: v2.Adapter}

    def __init__(self, version: int):
        self.adapter = self.adapters[version]()

    def parse(self, path: str):
        """
        Parse a sample from the given path using the appropriate adapter.

        :param path: The path of the sample to be parsed.
        :return: A generator, yielding first the user information and then the snapshots, one by one.
        """
        return self.adapter.parse(path)

    def build_dict(self, user_info, snapshot):
        """
        Build a dictionary representing one snapshot with user information, to be sent to the server.

        :param user_info: The user information to be sent.
        :param snapshot: The snapshot to be sent.
        :return: dictionary representing the snapshot with user information, to be sent to the server.
        """
        return self.adapter.build_dict(user_info, snapshot)

    def limit_snapshot_fields(self, snapshot, fields):
        """
        Remove unsupported fields from the given snapshot.

        :param snapshot: The snapshot to be transformed.
        :param fields: The list of supported fields.
        :return: A new snapshot, where non-supported fields have default values.
        """
        return self.adapter.limit(snapshot, fields)
