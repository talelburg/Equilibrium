import flask


def run_server(host, port, api_host, api_port):
    app = get_app(f"http://{api_host}:{api_port}")
    app.run(host=host, port=port, threaded=True)


def get_app(api_base):
    app = flask.Flask(__name__, static_folder="build/static", template_folder="build")
    app.config["api_base"] = api_base

    @app.route("/")
    def index():
        return flask.render_template("index.html", api_server=app.config["api_base"])

    return app
