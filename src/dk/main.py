import rich_click as click

from .commands import docker, sync
from .config import load_user_settings
from .theme import RICH_CLICK_HELP_CONFIG


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version="1.0.0")
@click.rich_config(help_config=RICH_CLICK_HELP_CONFIG)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    A CLI for MacOS local development utilities
    """
    user_settings = load_user_settings()
    ctx.obj = {"user_settings": user_settings}


cli.add_command(sync)
cli.add_command(docker)
