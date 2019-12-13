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


@client.command("run")
@click.argument("address", type=str)
@click.argument("sample_path", type=click.Path(exists=True, dir_okay=False))
def run_client(address, sample_path):
    equilibrium.upload_sample(normalize_address(address), sample_path)


@main.group()
def server():
    pass


@server.command("run")
@click.argument("port", type=int)
@click.argument("data_dir", type=click.Path(exists=True, file_okay=False))
def run_server(port, data_dir):
    equilibrium.Server(port, data_dir).run()


@main.command("read")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def read_sample(filename):
    info = equilibrium.sample.UserInformation.parse_file(filename)
    print(f"User {info.user_id}: {info.username}, born {info.birthdate:%B %d, %Y} ({info.gender})")

    def print_hook(obj, ctx):
        translation = (obj.translation.x, obj.translation.y, obj.translation.z)
        rotation = (obj.rotation.x, obj.rotation.y, obj.rotation.z, obj.rotation.w)
        print(f"Snapshot from {obj.timestamp:%B %d, %Y at %H:%M:%S.%f} at {translation} / {rotation} "
              f"with a {obj.color_image.width}x{obj.color_image.height} color image "
              f"and a {obj.depth_image.width}x{obj.depth_image.height} depth image")
        del obj

    equilibrium.Sample(print_hook).parse_file(filename)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
