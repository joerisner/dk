import sys
from pathlib import Path

import rich_click as click

from ..config import UserSettings
from ..utils import error, out, run_cmd, warn


def validate_directory(directory: Path) -> None:
    if not directory.exists():
        error(f"Could not find directory '{directory}'")
        sys.exit(1)

    rev_parse_cmd = run_cmd(["git", "-C", directory, "rev-parse"])

    if rev_parse_cmd.returncode != 0:
        error(f"'{directory}' is not a git repository")
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
    user_settings = click.get_current_context().obj["user_settings"]  # type: ignore

    if not user_settings or not user_settings.sync:
        error(msg="Missing required sync configuration", tip=UserSettings.model_fields["sync"].description or "")
        sys.exit(1)

    for repository in user_settings.sync.repositories:
        repository_path = Path.home() / user_settings.sync.directory / repository

        out(f"==> Updating [underline]{repository}[/underline]", style="highlight")
        validate_directory(repository_path)
        sync_repository(repository_path)
