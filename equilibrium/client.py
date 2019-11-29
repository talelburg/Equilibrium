import datetime
from typing import Tuple

from .thought import Thought
from .utils import Connection


def upload_thought(address: Tuple[str, int], user_id: int, thought: str):
    """
    Upload a user's thought to a server.

    :param address: The address of the server.
    :param user_id: The ID of the user who had the thought.
    :param thought: The contents of the thought.
    """
    thought = Thought(user_id, datetime.datetime.now(), thought)
    data = thought.serialize()
    with Connection.connect(*address) as connection:
        connection.send(data)
