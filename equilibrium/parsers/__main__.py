import sys
import time

import click

import equilibrium
from equilibrium.queue.queue_handler import QueueHandler
from equilibrium.sample import SampleHandler
from equilibrium.utils.cli import create_basic_cli

main, log = create_basic_cli()


@main.command("parse")
@click.argument("parser_name", type=str)
@click.argument("raw_data_path", type=click.Path(dir_okay=False, exists=True))
def parse(parser_name, raw_data_path):
    with open(raw_data_path, "r") as f:
        data = f.read()
    print(equilibrium.parsers.run_parser(parser_name, data))


@main.command("run-parser")
@click.argument("parser_name", type=str)
@click.argument("url", type=str)
def run_parser(parser_name, url):
    def callback(channel, method, properties, body):
        log(f"Received message {body} from queue {parser_name} at {url} for parsing")
        processed_data = equilibrium.parsers.run_parser(parser_name, body)
        handler = QueueHandler(url)
        log(f"Publishing message {processed_data} to queue at {url} after processing")
        handler.publish(exchange="processed", body=processed_data)

    log(f"Waiting to consume messages from queue {parser_name} at {url} and parse them")
    queue_handler = QueueHandler(url)
    queue_handler.consume(exchange="needs_parsing", queue=parser_name, callback=callback)


if __name__ == "__main__":
    try:
        main(prog_name="equilibrium-parsers")
    except Exception as error:
        log(f"Error: {error}")
        sys.exit(1)
