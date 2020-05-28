import sys

import click

from equilibrium.server import run_server
from equilibrium.utils.general.cli import create_basic_cli
from equilibrium.utils.queue import QueueHandler

main, log = create_basic_cli()


@main.command("run-server")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.option("-mq", "--message-queue", type=str, default="rabbitmq://127.0.0.1:5672")
def run_server_cli(host, port, message_queue):
    def publish(message):
        queue_handler = QueueHandler(message_queue)
        log(f"Publishing message {message} to queue at {message_queue} to be parsed")
        queue_handler.publish(exchange="needs_parsing", body=message)

    log(f"Setting up server at {host}:{port} to publish to message-queue at {message_queue}")
    run_server(host=host, port=port, publish=publish)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium.server")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
