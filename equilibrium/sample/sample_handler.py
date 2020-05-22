from equilibrium.sample import v2


class SampleHandler:
    """
    A class to handle operation on samples. Uses an adapter based on sample version.
    """
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

    def build_dict(self, d):
        """
        Build a BSON-able dictionary from relevant data from the sample.

        :param d: A dictionary of relevant data.
        :return: A BSON-able dictionary.
        """
        return self.adapter.build_dict(d)

    def recover_dict(self, d):
        """
        Recover relevant data from a BSON-able dictionary.

        :param d: The BSON-able dictionary.
        :return: A dictionary of relevant data.
        """
        return self.adapter.recover_dict(d)

    def build_message(self, *args, **kwargs):
        """
        Build a message, intended to be published to a message queue, from relevant data from the sample.
        """
        return self.adapter.build_message(*args, **kwargs)
