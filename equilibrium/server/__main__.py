import datetime
import json
import os
import pathlib
import sys
import traceback

import click
import pika
from google.protobuf.json_format import MessageToJson

import equilibrium
from equilibrium.queue.queue_handler import QueueHandler


class Log:
    def __init__(self):
        self.quiet = False
        self.include_traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.include_traceback and sys.exc_info():
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


log = Log()


@click.group()
@click.version_option(equilibrium.version)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-t", "--include_traceback", is_flag=True)
def main(quiet=False, include_traceback=False):
    log.quiet = quiet
    log.include_traceback = include_traceback


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
