import sys
from pathlib import Path
from typing import Any

import click

from ..utils import error, out, run_cmd, warn


def validate_config(config: Any) -> None:
    if config is None or "sync" not in config or config["sync"] is None:
        error(
            msg="Missing required sync configuration",
            tip="Add a 'sync' node to the dk config file to sync repositories",
        )
        sys.exit(1)

    if "projects_dir" not in config["sync"]:
        error(
            msg="Missing required 'projects_dir' value in sync configuration",
            tip="Assign to 'projects_dir' the directory (relative to HOME) where your projects are found",
        )
        sys.exit(1)

    if "repositories" not in config["sync"]:
        error(
            msg="Missing required 'repositories' list in sync configuration",
            tip="Assign to 'repositories' a list of projects to sync",
        )
        sys.exit(1)


def get_config() -> dict[str, Any]:
    config = click.get_current_context().obj["config"]
    validate_config(config)

    return {
        "projects_dir": config["sync"]["projects_dir"],
        "repositories": config["sync"]["repositories"],
    }


def validate_directory(directory: Path) -> None:
    if not directory.exists():
        error(f"Could not find directory '{directory}'")
        sys.exit(1)

    rev_parse_cmd = run_cmd(["git", "-C", directory, "rev-parse"])

    if rev_parse_cmd.returncode != 0:
        error(f"'{directory}' is not a git project")
        sys.exit(rev_parse_cmd.returncode)


def sync_repository(repository_path: Path) -> None:
    git_status = run_cmd(["git", "-C", repository_path, "status", "--porcelain"]).stdout

    if git_status:
        warn("Skipping this repo since there are local changes not yet committed")
        return

    all_branches = run_cmd(["git", "-C", repository_path, "remote", "show", "origin"]).stdout
    default_branch = run_cmd(["awk", "/HEAD branch/ {print $NF}"], input=all_branches).stdout

    out(msg=run_cmd(["git", "-C", repository_path, "checkout", default_branch]).stdout)
    out(run_cmd(["git", "-C", repository_path, "pull"]).stdout)


@click.command()
def sync():
    """Sync local git repositories with remote versions"""
    config = get_config()
    projects_dir = config["projects_dir"]
    repositories = config["repositories"]

    for repository in repositories:
        repository_path = Path.home() / projects_dir / repository

        out(f"==> Updating {repository}", style="highlight")
        validate_directory(repository_path)
        sync_repository(repository_path)
