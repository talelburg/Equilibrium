import json
import sys

import click

from equilibrium.saver import Saver
from equilibrium.utils.queue import QueueHandler
from equilibrium.utils.general.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("save")
@click.option("-d", "--database", type=str, default="mongodb://127.0.0.1:27017")
@click.argument("topic_name", type=str)
@click.argument("raw_data_path", type=click.Path(dir_okay=False, exists=True))
def save(topic_name, raw_data_path, database):
    with open(raw_data_path, "r") as f:
        data = f.read()
    print(Saver(database).save(topic_name, data))


@main.command("run-saver")
@click.option("-d", "--database", type=str, default="mongodb://127.0.0.1:27017")
@click.option("-mq", "--message-queue", type=str, default="rabbitmq://127.0.0.1:5672")
def run_saver(database, message_queue):
    def callback(message):
        log(f"Received message {message} from queue at {message_queue} for saving")
        topic, = json.loads(message)["result"].keys()
        log(f"Saving {topic} to database at {database}")
        Saver(database).save(topic, message)

    log(f"Waiting to consume processed data from {message_queue} and save it")
    queue_handler = QueueHandler(message_queue)
    queue_handler.consume(exchange="processed", queue="saver", callback=callback)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-saver")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
