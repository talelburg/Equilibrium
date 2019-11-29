import socket


class Connection:
    def __init__(self, sock: socket.socket):
        self.socket = sock

    def __repr__(self):
        sockname = self.socket.getsockname()
        peername = self.socket.getpeername()
        return f"<Connection from {sockname[0]}:{sockname[1]} to {peername[0]}:{peername[1]}>"

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.socket.close()

    @classmethod
    def connect(cls, host, port):
        sock = socket.socket()
        sock.connect((host, port))
        return cls(sock)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = b""
        while len(data) < size:
            new = self.socket.recv(size - len(data))
            if not new:
                raise Exception("Connection closed")
            data += new
        return data

    def close(self):
        self.socket.close()
