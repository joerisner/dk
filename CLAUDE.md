# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`dk` is a personal MacOS dev-environment CLI for running common user- and project-level scripts.

## Commands

```bash
task build        # build the project
task ci           # run all local CI checks (bin/ci)
task install      # sync the local .venv using uv
task test         # run tests
```

- Common commands are executed via Taskfile and can be found in the `taskfile.yml` file.
- Use `uv run` instead of direct `python` calls, when necessary.

## Architecture

### Click CLI

- `src/dk/config.py` - reads YAML from `~/.config/dk/config.yml` and project-level settings from `<project>/dk.yml`.
- `src/dk/commands/` - `click` commands are individual files.

## Code Review Rules

- Report findings with a confidence level and cite the exact `file:line` you verified against. If you cannot verify, say so instead of asserting.
- Flag newly-added files that aren't source or intentional config — scratch output, logs, session artifacts, stray dumps, etc.
