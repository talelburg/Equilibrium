import os
import sys
import traceback

import click

import equilibrium


class Log:
    def __init__(self):
        self.quiet = False
        self.include_traceback = False

    def __call__(self, message):
        if self.quiet:
            return
        if self.include_traceback and sys.exc_info():
            message += os.linesep + traceback.format_exc().strip()
        click.echo(message)


def create_basic_cli():
    log = Log()

    @click.group()
    @click.version_option(equilibrium.version)
    @click.option("-q", "--quiet", is_flag=True)
    @click.option("-t", "--include_traceback", is_flag=True)
    def main(quiet=False, include_traceback=False):
        log.quiet = quiet
        log.include_traceback = include_traceback

    return main, log
