import os
import sys
import traceback

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


log = Log()


@click.group()
@click.version_option(equilibrium.version)
@click.option("-q", "--quiet", is_flag=True)
@click.option("-t", "--include_traceback", is_flag=True)
def main(quiet=False, include_traceback=False):
    log.quiet = quiet
    log.include_traceback = include_traceback


@main.command("upload-sample")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.argument("sample_path", type=click.Path(exists=True, dir_okay=False))
def upload_sample(host, port, sample_path):
    log(f"Uploading sample at {sample_path} to {host}:{port}")
    equilibrium.client.upload_sample(host=host, port=port, path=sample_path)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
