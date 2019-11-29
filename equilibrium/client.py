import datetime

from .thought import Thought
from .utils import Connection


def upload_thought(address, user_id, thought):
    thought = Thought(user_id, datetime.datetime.now(), thought)
    data = thought.serialize()
    with Connection.connect(*address) as connection:
        connection.send(data)
