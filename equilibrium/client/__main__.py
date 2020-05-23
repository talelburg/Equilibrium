import sys

import click

import equilibrium
from equilibrium.utils.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("upload-sample")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.argument("sample_path", type=click.Path(exists=True, dir_okay=False))
def upload_sample(host, port, sample_path):
    log(f"Uploading sample at {sample_path} to {host}:{port}")
    equilibrium.client.upload_sample(host=host, port=port, path=sample_path)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-client")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
