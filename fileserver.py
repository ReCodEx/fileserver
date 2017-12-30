#!/usr/bin/env python3

import click
import signal

from fileserver import create_app


@click.group()
def cli():
    pass


@cli.command()
@click.option("--directory")
def runserver(directory=None):
    def shutdown(*args, **kwargs):
        raise KeyboardInterrupt

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    app = create_app(directory)
    app.run()


if __name__ == "__main__":
    cli()
