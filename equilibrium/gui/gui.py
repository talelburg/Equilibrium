import flask

from equilibrium.utils.general.wait_for_tcp_port import wait_for_port

app = flask.Flask(__name__, static_folder="build/static", template_folder="build")


@app.route("/")
def index():
    return flask.render_template("index.html", api_server=app.config["api_base"])


def run_server(host, port, api_host, api_port):
    app.config["api_base"] = f"http://{api_host}:{api_port}"
    app.run(host=host, port=port, threaded=True)
