import datetime
import struct


class Thought:
    def __init__(self, user_id, timestamp, thought):
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

    def serialize(self):
        return struct.pack("LLI", self.user_id, int(self.timestamp.timestamp()),
                           len(self.thought)) + self.thought.encode()

    @classmethod
    def deserialize(cls, data):
        user_id, timestamp, thought_length = struct.unpack("LLI", data[:20])
        return cls(user_id, datetime.datetime.fromtimestamp(timestamp), data[20:].decode())
