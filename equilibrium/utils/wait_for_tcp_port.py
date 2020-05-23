import time
import socket


def wait_for_port(host: str, port: int, timeout: float = 30.0):
    """
    Wait until host starts accepting connections on specified port.

    :param host:  Host address on which the port should exist.
    :param port: The port number to wait for.
    :param timeout: How long to wait before raising an error, in seconds.
    :raises TimeoutError: If host:port isn't accepting connections after the time specified in `timeout`.
    """
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError(f"Waited too long for {host}:{port} to accept connections") from ex
