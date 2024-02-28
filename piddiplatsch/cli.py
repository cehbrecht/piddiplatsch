"""Console script for piddiplatsch."""

import sys
import os
import click

from piddiplatsch.consumer import consume_topic as do_consume
from piddiplatsch.send import send_topic as do_send

CONTEXT_OBJ = dict()
CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"], obj=CONTEXT_OBJ)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def cli(ctx):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)


@cli.command()
@click.pass_context
def consume(ctx):
    click.echo("Starting consumer ...")
    try:
        do_consume()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


@cli.command()
@click.pass_context
def send(ctx):
    click.echo("Send to queue ...")
    do_send()


if __name__ == "__main__":
    cli(obj={})
