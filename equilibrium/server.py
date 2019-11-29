import pathlib
import struct
import threading
from datetime import datetime

from .utils import Listener


def run_server(address, data_dir):
    data_path = pathlib.Path(data_dir)
    if not data_path.exists():
        data_path.mkdir(parents=True)
    with Listener(address[1], host=address[0]) as listen:
        while True:
            conn = listen.accept()
            handler = ClientHandler(conn, data_path)
            handler.start()


class ClientHandler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, connection, data_path):
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
