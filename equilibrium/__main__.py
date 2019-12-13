import datetime
import os
import pathlib
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
    equilibrium.run_server(port, data_dir)


@main.command("read")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
@click.argument('version', type=int, default=2)
def read_sample(filename, version):
    versions = {1: read_sample_v1, 2: read_sample_v2}
    versions[version](filename)


def read_sample_v1(filename):
    info = equilibrium.sample.v1.UserInformation.parse_file(filename)
    print(f"User {info.user_id}: {info.username}, born {info.birthdate:%B %d, %Y} ({info.gender})")

    def print_hook(obj, ctx):
        translation = (obj.translation.x, obj.translation.y, obj.translation.z)
        rotation = (obj.rotation.x, obj.rotation.y, obj.rotation.z, obj.rotation.w)
        print(f"Snapshot from {obj.timestamp:%B %d, %Y at %H:%M:%S.%f} at {translation} / {rotation} "
              f"with a {obj.color_image.width}x{obj.color_image.height} color image "
              f"and a {obj.depth_image.width}x{obj.depth_image.height} depth image")
        del obj

    equilibrium.sample.v1.Sample(print_hook).parse_file(filename)


def read_sample_v2(filename):
    sample = equilibrium.sample.SampleReader(2).parse(filename)
    print(f"User {sample.user.user_id}: {sample.user.username}, "
          f"born {datetime.datetime.fromtimestamp(sample.user.birthday):%B %d, %Y} ({sample.user.gender})")
    for snapshot in sample.snapshots:
        pose = snapshot.pose
        translation = (pose.translation.x, pose.translation.y, pose.translation.z)
        rotation = (pose.rotation.x, pose.rotation.y, pose.rotation.z, pose.rotation.w)
        print(f"Snapshot from {datetime.datetime.fromtimestamp(snapshot.datetime / 1000):%B %d, %Y at %H:%M:%S.%f}"
              f" at {translation} / {rotation} with a {snapshot.color_image.width}x{snapshot.color_image.height}"
              f" color image and a {snapshot.depth_image.width}x{snapshot.depth_image.height} depth image, feeling"
              f" hunger: {snapshot.feelings.hunger}, thirst: {snapshot.feelings.thirst},"
              f" exhaustion: {snapshot.feelings.exhaustion}, happiness: {snapshot.feelings.happiness}")


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
