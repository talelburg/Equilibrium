import datetime
import struct

import pytz

FORMAT = "<qqI"
HEADER_SIZE = struct.calcsize(FORMAT)


class Thought:
    """
    A class representing a user's thought.
    """

    def __init__(self, user_id: int, timestamp: datetime.datetime, thought: str):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f"Thought(user_id={self.user_id!r}, timestamp={self.timestamp!r}, thought={self.thought!r})"

    def __str__(self):
        return f'[{self.timestamp:%Y-%m-%d %H:%M:%S}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self) -> bytes:
        """
        Serialize a thought to a compact representation, suitable for sending over networks.

        :return: Bytes representing the thought.
        """
        return struct.pack(FORMAT, self.user_id, int(self.timestamp.timestamp()),
                           len(self.thought)) + self.thought.encode()

    @classmethod
    def deserialize(cls, data: bytes):
        """
        Deserialize bytes into a thought object.

        :param data: Bytes to be deserialized.
        :return: The generated thought.
        """
        user_id, timestamp, thought_length = struct.unpack(FORMAT, data[:HEADER_SIZE])
        return cls(user_id, datetime.datetime.fromtimestamp(timestamp, tz=pytz.utc), data[HEADER_SIZE:].decode())
