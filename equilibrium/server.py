import json
import pathlib
import threading
from functools import wraps

from PIL import Image

from .protocol import Hello, Config, Snapshot
from .utils import Connection, Listener


class Server:
    fields = {}

    def __init__(self, port: int, data_dir: str):
        """
        Set up a server, which will listen for and handle incoming connections until interrupted.

        :param port: The port to bind the server to.
        :param data_dir: The path to the directory for the server to store data in.
        """
        self.port = port
        self.data_path = pathlib.Path(data_dir)

    def run(self):
        """
        Actually run the server.
        """
        if not self.data_path.exists():
            self.data_path.mkdir(parents=True)
        with Listener(self.port) as listen:
            while True:
                print("Waiting for connection...")
                conn = listen.accept()
                handler = ClientHandler(conn, self.data_path)
                handler.start()

    @classmethod
    def parses(cls, field_name: str):
        """
        Decorator to register parsers for snapshot fields.
        """

        def decorator(f):
            cls.fields[field_name] = f

            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)

            return wrapper

        return decorator

    @classmethod
    def parse(cls, directory: pathlib.Path, snapshot):
        """
        Parse a given snapshot. Calls registered parsers on received arguments.
        """
        for parser in cls.fields.values():
            parser(directory, snapshot)


@Server.parses("translation")
def parse_translation(directory, snapshot):
    translation = snapshot.translation
    with open(directory / "translation.json", "w") as f:
        json.dump({"x": translation.x, "y": translation.y, "z": translation.z}, f, indent=4)


@Server.parses("color_image")
def parse_color_image(directory, snapshot):
    color_image = snapshot.color_image
    image = Image.new("RGB", (color_image.width, color_image.height))
    image.putdata([(pixel.red, pixel.green, pixel.blue) for pixel in color_image.data])
    image.save(str(directory / "color_image.jpg"))


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
        print("Connection thread started")
        print("Receiving hello message")
        hello_message = self.connection.receive_message()
        hello = Hello.parse(hello_message)
        user_path = self.data_path / f'{hello.user_id}'
        if not user_path.exists():
            user_path.mkdir()
        config = Config.build({"fields": list(Server.fields.keys())})
        print("Sending config message")
        self.connection.send_message(config)
        print("Receiving snapshot message")
        snapshot_message = self.connection.receive_message()
        snapshot = Snapshot.parse(snapshot_message)
        snapshot_path = user_path / f'{snapshot.timestamp:%Y-%m-%d_%H-%M-%S-%f}'
        if not snapshot_path.exists():
            snapshot_path.mkdir()
        with self.lock:
            print("Parsing snapshot fields")
            Server.parse(snapshot_path, snapshot)
        print("Closing connection")
        self.connection.close()
