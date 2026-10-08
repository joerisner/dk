import os
import sys
from pathlib import Path
from typing import Any

import yaml

from .utils import error, out


def get_config_file_path() -> Path:
    default_path = Path.home() / ".config" / "dk" / "config.yml"
    return Path(os.getenv("DK_CONFIG_FILE", default_path))


def load_config() -> Any:
    try:
        config_file = get_config_file_path()
        with open(config_file) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        error("No config file found")
        out("\nSet DK_CONFIG_FILE or create a new config file at '$HOME/.config/dk/config.yml'")
        sys.exit(1)
