# dk

`dk` is CLI, written in Python, that manages my local MacOS development environment.

### Installation and usage

Install dk as a `uv` tool.

```sh
uv tool install git+https://github.com/joerisner/dk
```

Once dk is installed, as long as your `uv` tool bin dir is on your `PATH`, you should be able to run dk without issue.

```sh
dk --help
```

## Development

This project uses `uv` for managing Python versions, dependencies, and the project's environment. Run the setup script to get started with `uv`.

```sh
task setup
```

Once the project is setup with `uv`, create the virtual environment and install dependencies.

```sh
task install
```

See additional tasks by viewing the [Taskfile](./taskfile.yml) or by running `task`.

### Using the CLI

During development, use `uv` to run `dk`.

```sh
uv run dk --help
```
