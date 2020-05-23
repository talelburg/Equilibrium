from equilibrium.sample import gzip_protobuf


class SampleHandler:
    """
    A class to handle operation on samples. Uses an adapter based on sample version.
    """
    adapters = {"gzip_protobuf": gzip_protobuf.Adapter}

    def __init__(self, version):
        self.adapter = self.adapters[version]

    def parse(self, path):
        """
        Parse a sample from the given path using the appropriate adapter.

        :param path: The path of the sample to be parsed.
        :return: A generator, yielding first the user information and then the snapshots, one by one.
        """
        return self.adapter.parse(path)

    def data_to_dict(self, data):
        """
        Build a BSON-able dictionary from relevant data from the sample.

        :param data: A dictionary of relevant data.
        :return: A BSON-able dictionary.
        """
        return self.adapter.data_to_dict(data)

    def dict_to_data(self, dictionary):
        """
        Recover relevant data from a BSON-able dictionary.

        :param dictionary: The BSON-able dictionary.
        :return: A dictionary of relevant data.
        """
        return self.adapter.dict_to_data(dictionary)

    def data_to_json(self, data):
        """
        Build a JSON-able dictionary, intended to be published to a message-queue, with provided data.

        Large fields are saved to disk to avoid large messages.

        :param data: The relevant data.
        :return: The constructed JSON-able dictionary.
        """
        return self.adapter.data_to_json(data)

    def json_to_data(self, json_dict):
        """
        Parses the provided JSON-able dictionary, assumed to have been consumed from a message-queue, into data.

        Large fields are saved to disk to avoid large messages.

        :param json_dict: The relevant JSON-able dictionary.
        :return: The parsed data.
        """
        return self.adapter.json_to_data(json_dict)
