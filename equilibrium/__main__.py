import os
import sys
import traceback
from typing import Tuple

import click

import equilibrium


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


def normalize_address(address: str) -> Tuple[str, int]:
    ip, port_str = address.split(":")
    return ip, int(port_str)


log = Log()


@click.group()
@click.version_option(equilibrium.version)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-t", "--include_traceback", is_flag=True)
def main(quiet=False, include_traceback=False):
    log.quiet = quiet
    log.include_traceback = include_traceback


@main.group()
def client():
    pass


@client.command("upload")
@click.argument("address", type=str)
@click.argument("user_id", type=int)
@click.argument("thought", type=str)
def client_upload(address, user_id, thought):
    equilibrium.upload_thought(normalize_address(address), user_id, thought)


@main.group()
def server():
    pass


@server.command("run")
@click.argument("address", type=str)
@click.argument("data_dir", type=str)
def server_run(address, data_dir):
    equilibrium.run_server(normalize_address(address), data_dir)


@main.group()
def web():
    pass


@web.command("run")
@click.argument("address", type=str)
@click.argument("data_dir", type=str)
def web_run(address, data_dir):
    equilibrium.run_webserver(normalize_address(address), data_dir)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
