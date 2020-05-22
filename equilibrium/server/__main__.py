import datetime
import pathlib
import sys

import click

import equilibrium
from equilibrium.queue.queue_handler import QueueHandler
from equilibrium.utils.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("run-server")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.argument("url", type=str)
def run_server(host, port, url):
    def publish(data):
        user_info = data["user_information"]
        snapshot = data["snapshot"]

        timestamp = datetime.datetime.fromtimestamp(snapshot.datetime / 1000)
        snapshot_path = pathlib.Path(f"/home/user/Desktop/data/{user_info.user_id}/{timestamp:%Y-%m-%d_%H-%M-%S-%f}")
        snapshot_path.mkdir(parents=True, exist_ok=True)
        message = equilibrium.sample.SampleHandler(2).build_message(user_info, snapshot, str(snapshot_path))

        queue_handler = QueueHandler(url)
        queue_handler.publish(exchange="", routing_key="snapshots", body=message)
        log(f"Published message {message} to queue at {url}")

    log(f"Setting up server at {host}:{port} to publish to {url}")
    equilibrium.server.run_server(host=host, port=port, publish=publish)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
