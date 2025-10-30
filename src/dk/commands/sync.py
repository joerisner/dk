import inspect
import sys
from pathlib import Path

import click

from ..utils import error, out, run_cmd


def validate_config(config):
    if config is None or 'sync' not in config or config['sync'] is None or 'repositories' not in config['sync']:
        error("Missing required 'sync' configuration")
        out("\nAdd a 'sync' node to the config file with a list of repositories to sync. For example:\n")
        out(
            inspect.cleandoc("""
            sync:
              repositories:
                - foo
                - bar
            """)
        )
        sys.exit(1)


def get_repos_from_config():
    config = click.get_current_context().obj['config']
    validate_config(config)

    return config['sync']['repositories']


def validate_directory(directory):
    if not directory.exists():
        error(f"Could not find directory '{directory}'")
        sys.exit(1)

    rev_parse_cmd = run_cmd(['git', '-C', directory, 'rev-parse'])

    if rev_parse_cmd.returncode != 0:
        error(f'{directory} is not a git project')
        sys.exit(rev_parse_cmd.returncode)


def sync_repository(repository_path):
    git_status = run_cmd(['git', '-C', repository_path, 'status', '--porcelain'], return_output=True)

    if git_status:
        out('Skipping this repo since there are local changes not yet committed', style='warn')
        return

    all_branches = run_cmd(['git', '-C', repository_path, 'remote', 'show', 'origin'], return_output=True)
    default_branch = run_cmd(['awk', '/HEAD branch/ {print $NF}'], input=all_branches, return_output=True)

    run_cmd(['git', '-C', repository_path, 'checkout', default_branch], print_output=True)
    run_cmd(['git', '-C', repository_path, 'pull'], print_output=True)


@click.command()
def sync():
    """Sync local git repositories with remote versions"""
    repositories = get_repos_from_config()

    for repository in repositories:
        repository_path = Path.home() / 'projects' / repository

        out(f'==> Updating {repository}', style='highlight')
        validate_directory(repository_path)
        sync_repository(repository_path)
