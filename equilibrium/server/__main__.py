import json
import sys

import click

import equilibrium
from equilibrium.queue.queue_handler import QueueHandler
from equilibrium.sample import SampleHandler
from equilibrium.utils.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("run-server")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.argument("url", type=str)
def run_server(host, port, url):
    def publish(data):
        message = json.dumps(SampleHandler("gzip_protobuf").data_to_json(data))
        queue_handler = QueueHandler(url)
        log(f"Publishing message {message} to queue at {url} to be parsed")
        queue_handler.publish(exchange="needs_parsing", body=message)

    log(f"Setting up server at {host}:{port} to publish to message-queue at {url}")
    equilibrium.server.run_server(host=host, port=port, publish=publish)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-server")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
