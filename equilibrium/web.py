import pathlib
from typing import Tuple

import flask

app = flask.Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    users = sorted(user_dir.name for user_dir in app.config["data_path"].iterdir())
    return flask.render_template('/index.html', title="Equilibrium BCI", users=users)


@app.route("/users/<user_id>")
def user_page(user_id):
    user_path = app.config["data_path"] / user_id
    if not user_path.exists():
        return 404
    rows = []
    for timestamp_path in user_path.iterdir():
        date_parts = timestamp_path.name.split("_")
        timestamp = f"{date_parts[0]} {date_parts[1].replace('-', ':').replace('.txt', '')}"
        rows.append((timestamp, timestamp_path.read_text()))
    rows = sorted(rows, key=lambda p: p[0])
    return flask.render_template('/user.html', title=f"Equilibrium BCI: User {user_id}", rows=rows)


def run_webserver(address: Tuple[str, int], data_dir: str):
    """
    Set up a web server, which will serve the data contained in the given folder.

    :param address: The address to bind the server to.
    :param data_dir: The path to the directory for the server to load data from.
    """
    data_path = pathlib.Path(data_dir)
    app.config["data_path"] = data_path
    app.run(host=address[0], port=address[1])
