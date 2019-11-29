import pathlib
import struct
import threading
from datetime import datetime
from typing import Tuple

from .utils import Connection, Listener


def run_server(address: Tuple[str, int], data_dir: str):
    """
    Set up a server, which will listen for and handle incoming connections until interrupted.

    :param address: The address to bind the server to.
    :param data_dir: The path to the directory for the server to store data in.
    """
    data_path = pathlib.Path(data_dir)
    if not data_path.exists():
        data_path.mkdir(parents=True)
    with Listener(address[1], host=address[0]) as listen:
        while True:
            conn = listen.accept()
            handler = ClientHandler(conn, data_path)
            handler.start()


class ClientHandler(threading.Thread):
    """
    A specialized thread to handle incoming connections to the server.
    """
    lock = threading.Lock()

    def __init__(self, connection: Connection, data_path: pathlib.Path):
        super().__init__()
        self.connection = connection
        self.data_path = data_path

    def run(self):
        data = self.connection.receive(20)
        user_id, timestamp, thought_size = struct.unpack('LLI', data)
        user_path = self.data_path / f'{user_id}'
        if not user_path.exists():
            user_path.mkdir()
        thought = self.connection.receive(thought_size)
        file_path = user_path / f'{datetime.fromtimestamp(timestamp):%Y-%m-%d_%H-%M-%S}.txt'
        if not file_path.exists():
            file_path.touch()
        with self.lock:
            thoughts = list(filter(None, file_path.read_text().split('\n')))
            thoughts.append(thought.decode())
            data = '\n'.join(thoughts)
            file_path.write_text(f'{data}')
        self.connection.close()
