# dk

CLI tool providing convenience scripts for my local development.

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

This project uses `uv` for managing Python versions, dependencies, and the project's environment. Run the (opinionated) `setup` target to get started with `uv`.

```sh
make setup
```

Once the project is setup with `uv`, create the virtual environment and install dependencies.

```sh
make install
```

See additional `make` targets by viewing the [Makefile](./Makefile) or by running `make help` (or just `make`).

### Using the CLI

During development, use `uv` to run `dk`.

```sh
uv run dk --help
```
