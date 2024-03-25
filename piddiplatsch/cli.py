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
@click.option("--port", "-p", type=int, default="5672", help="The rabbitmq port.")
@click.option("--exchange", "-e", default="pids", help="The exchange topic.")
@click.option(
    "--handler",
    "-P",
    type=click.Choice(["all", "wdcc", "cmip6"], case_sensitive=False),
    multiple=True,
    default=["all"],
    help="Choose which handlers should be used.",
)
@click.option("--dry-run", is_flag=True, help="Use dry run mode.")
@click.pass_context
def consume(ctx, host, port, exchange, handler, dry_run):
    click.echo("Starting consumer ...")
    try:
        do_consume(host, port, exchange, handler, dry_run)
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


@cli.command()
@click.pass_context
@click.option("--host", "-H", default="localhost", help="The rabbitmq hostname.")
@click.option("--port", "-p", type=int, default="5672", help="The rabbitmq port.")
@click.option("--exchange", "-e", default="pids", help="The exchange topic.")
@click.option("--routing_key", "-k", default="wdcc.test", help="The routing key.")
@click.argument("file", type=click.Path(exists=True))
def send(ctx, host, port, exchange, routing_key, file):
    click.echo("Send to queue ...")
    do_send(host, port, exchange, routing_key, file)


if __name__ == "__main__":
    cli(obj={})
