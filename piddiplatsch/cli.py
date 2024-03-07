"""Console script for piddiplatsch."""

import sys
import os
import click

from piddiplatsch.consumer import do_consume
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
@click.option("--host", "-H", default="localhost", help="The rabbitmq hostname.")
@click.option("--queue", "-q", default="birds", help="The queue name.")
@click.option("--exchange", "-e", default="topic_birds", help="The exchange topic.")
@click.option("--routing_key", "-k", default="bird.*", help="The routing key.")
@click.option("--type", "-t", default="default", help="The consumer type.")
@click.pass_context
def consume(ctx, host, queue, exchange, routing_key, type):
    click.echo("Starting consumer ...")
    try:
        do_consume(host, queue, exchange, routing_key, type)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


@cli.command()
@click.pass_context
@click.option("--exchange", "-e", default="topic_birds", help="The exchange topic.")
@click.option("--routing_key", "-k", default="bird.penguin", help="The routing key.")
@click.option(
    "--message", "-m", default="Hello World", help="A message you like to send."
)
def send(ctx, exchange, routing_key, message):
    click.echo("Send to queue ...")
    do_send(exchange, routing_key, message)


if __name__ == "__main__":
    cli(obj={})
