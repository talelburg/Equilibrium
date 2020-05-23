import sys

import click

from equilibrium.parsers import run_parser
from equilibrium.utils.general.cli import create_basic_cli
from equilibrium.utils.queue import QueueHandler

main, log = create_basic_cli()


@main.command("parse")
@click.argument("parser_name", type=str)
@click.argument("raw_data_path", type=click.Path(dir_okay=False, exists=True))
def parse(parser_name, raw_data_path):
    with open(raw_data_path, "r") as f:
        data = f.read()
    print(run_parser(parser_name, data))


@main.command("run-parser")
@click.argument("parser_name", type=str)
@click.option("-mq", "--message-queue", type=str, default="rabbitmq:127.0.0.1:5672")
def run_parser_cli(parser_name, message_queue):
    def callback(message):
        log(f"Received message {message} from queue {parser_name} at {message_queue} for parsing")
        processed_data = run_parser(parser_name, message)
        handler = QueueHandler(message_queue)
        log(f"Publishing message {processed_data} to queue at {message_queue} after processing")
        handler.publish(exchange="processed", body=processed_data)

    log(f"Waiting to consume messages from queue {parser_name} at {message_queue} and parse them")
    queue_handler = QueueHandler(message_queue)
    queue_handler.consume(exchange="needs_parsing", queue=parser_name, callback=callback)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-parsers")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
