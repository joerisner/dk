import sys

import rich_click as click

from ..utils import error, run_cmd, success


def run_docker(*args: str) -> str:
    """Helper for running `docker` commands"""
    process = run_cmd(["docker", *args])

    if process.returncode != 0:
        # Truncate long error message from Docker to first 142 chars.
        error(f"`[highlight]docker {' '.join(args)}[/highlight]` failed", tip=process.stderr[:142])
        sys.exit(process.returncode)

    return process.stdout


@click.group()
def docker():
    """Run Docker-related utilities (requires subcommand)"""


@docker.command()
@click.confirmation_option(prompt="This removes ALL containers, images, and volumes. Continue?")
def prune():
    """Remove all containers, images, and volumes (destructive!)"""
    containers = run_docker("ps", "--all", "--quiet")

    if containers:
        run_docker("stop", "--timeout", "0", *containers.split())

    run_docker("system", "prune", "--all", "--force")
    run_docker("volume", "prune", "--all", "--force")

    success("Removed all containers, images, and volumes")
