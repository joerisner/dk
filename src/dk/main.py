import click

from .commands.sync import sync
from .config import load_config

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option()
@click.pass_context
def cli(ctx):
    """A CLI for local development conveniences"""
    config = load_config()
    ctx.obj = {'config': config}


cli.add_command(sync)
