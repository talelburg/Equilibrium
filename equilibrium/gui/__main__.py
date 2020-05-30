import sys

import click

from equilibrium.gui import run_server
from equilibrium.utils.general.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("run-server")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8080)
@click.option("-H", "--api-host", type=str, default="127.0.0.1")
@click.option("-P", "--api-port", type=int, default=5000)
def run_server_cli(host, port, api_host, api_port):
    log(f"Setting up gui server at {host}:{port} to serve data from {api_host}:{api_port}")
    run_server(host=host, port=port, api_host=api_host, api_port=api_port)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium.gui")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
