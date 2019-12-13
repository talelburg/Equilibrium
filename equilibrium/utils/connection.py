import socket

from construct import Struct, Default, Int32ul, len_, this, Bytes

Message = Struct(
    length=Default(Int32ul, len_(this.message)),
    message=Bytes(this.length),
)


class Connection:
    """
    A helper class to manage network connections.
    """

    def __init__(self, sock: socket.socket):
        self.socket = sock

    def __repr__(self):
        sockname = self.socket.getsockname()
        peername = self.socket.getpeername()
        return f"<Connection from {sockname[0]}:{sockname[1]} to {peername[0]}:{peername[1]}>"

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host: str, port: int):
        """
        Instantiate a new connection with the supplied parameters.

        :param host: The host to connect to.
        :param port: The port to access the host with.
        :return: The created Connection object.
        """
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def send(self, data: bytes):
        """
        Send all supplied data over the connection.

        :param data: The data to be sent.
        """
        self.socket.sendall(data)

    def send_message(self, data: bytes):
        self.send(Message.build({"message": data}))

    def receive(self, size: int) -> bytes:
        """
        Read data from the connection until a specific size has been read.

        :param size: The amount of data to be read.
        :return: The data read.
        :raises RuntimeError: If the connection closes before all of the data was read.
        """
        data = b""
        while len(data) < size:
            new = self.socket.recv(size - len(data))
            if not new:
                raise RuntimeError("Connection closed")
            data += new
        return data

    def receive_message(self) -> bytes:
        data = self.receive(4)
        message_size = Int32ul.parse(data)
        data += self.receive(message_size)
        return Message.parse(data).message

    def close(self):
        self.socket.close()
