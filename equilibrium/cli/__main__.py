import base64
import json
import sys

import click
import requests

from equilibrium.utils.general.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("get-users")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=5000)
def get_users(host, port):
    r = requests.get(f"http://{host}:{port}/users")
    print(r.json())


@main.command("get-user")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=5000)
@click.argument("user_id", type=int)
def get_user(host, port, user_id):
    r = requests.get(f"http://{host}:{port}/users/{user_id}")
    print(r.json())


@main.command("get-snapshots")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=5000)
@click.argument("user_id", type=int)
def get_snapshots(host, port, user_id):
    r = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots")
    print(r.json())


@main.command("get-snapshot")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=5000)
@click.argument("user_id", type=int)
@click.argument("timestamp", type=int)
def get_snapshot(host, port, user_id, timestamp):
    r = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{timestamp}")
    print(r.json())


@main.command("get-result")
@click.option("-h", "--host", type=str, default="127.0.0.1")
@click.option("-p", "--port", type=int, default=5000)
@click.argument("user_id", type=int)
@click.argument("timestamp", type=int)
@click.argument("result_name", type=str)
@click.option("-s", "--save", type=click.Path(dir_okay=False, writable=True))
def get_result(host, port, user_id, timestamp, result_name, save):
    r = requests.get(f"http://{host}:{port}/users/{user_id}/snapshots/{timestamp}/{result_name}")
    result = r.json()
    print(result)
    if save:
        if "data" in result:
            r = requests.get(f"http://{host}:{port}{result['data']}")
            result = r.json()["data"]
            data = base64.b64decode(result)
            with open(save, "wb") as f:
                f.write(data)
        else:
            with open(save, "w") as f:
                json.dump(result, f, indent=4)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium.cli")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
