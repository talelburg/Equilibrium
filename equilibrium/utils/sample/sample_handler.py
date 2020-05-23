import pathlib

from equilibrium.utils.sample.gzip_protobuf import GzipAdapter


class SampleHandler:
    """
    A class to handle operation on samples. Uses an adapter based on sample version.
    """
    adapters = {".gz": GzipAdapter}

    @classmethod
    def parse(cls, path):
        """
        Parse a sample from the given path using the appropriate adapter.

        :param path: The path of the sample to be parsed.
        :return: A generator, yielding first the user information and then the snapshots, one by one.
        """
        adapter = cls.adapters[pathlib.Path(path).suffix]
        return adapter.parse(path)

    @classmethod
    def data_to_full_json(cls, sample_format, data):
        """
        Build a JSON-able dictionary from relevant data from the sample.

        :param sample_format: The sample format dealt with.
        :param data: A dictionary of relevant data.
        :return: A BSON-able dictionary.
        """
        return cls.adapters[sample_format].data_to_full_json(data)

    @classmethod
    def data_to_light_json(cls, sample_format, data):
        """
        Build a JSON-able dictionary, intended to be published to a message-queue, with provided data.

        Large fields are saved to disk to avoid large messages.

        :param sample_format: The sample format dealt with.
        :param data: The relevant data.
        :return: The constructed JSON-able dictionary.
        """
        return cls.adapters[sample_format].data_to_light_json(data)

    @classmethod
    def json_to_data(cls, json_dict):
        """
        Parses the provided JSON-able dictionary, assumed to have been consumed from a message-queue, into data.

        :param json_dict: The relevant JSON-able dictionary.
        :return: The parsed data.
        """
        return cls.adapters[json_dict["sample_format"]].json_to_data(json_dict)
