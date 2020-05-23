import sys

import click

from equilibrium.api import run_api_server
from equilibrium.utils.general.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("run-server")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=8000)
@click.option("-d", "--database", type=str, default="mongodb://127.0.0.1:27017")
def run_server_cli(host, port, database):
    log(f"Setting up api server at {host}:{port} to serve data from {database}")
    run_api_server(host=host, port=port, database_url=database)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-api")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
