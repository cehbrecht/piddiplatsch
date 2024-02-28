"""Console script for piddiplatsch."""

import sys
import os
import click
from piddiplatsch.consumer import consume


@click.command()
def main(args=None):
    """Console script for piddiplatsch."""
    click.echo("Starting consumer ...")
    consume()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
