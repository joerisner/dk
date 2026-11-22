import sys
from pathlib import Path
from typing import get_args

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .utils import error

USER_CONFIG_FILE_PATH = Path.home() / ".config" / "dk" / "config.yml"


class SyncSettings(BaseModel):
    """Required settings for the `sync` command."""

    model_config = ConfigDict(extra="forbid")

    directory: Path = Field(description="Assign to `directory` the dir (relative to HOME) where your repos are found")
    repositories: list[str] = Field(description="Assign to `repositories` a list of repos to sync")


class UserSettings(BaseModel):
    """User-level configuration settings for dk."""

    sync: SyncSettings | None = Field(
        default=None,
        description="Add a `sync` node to the dk config file to sync repos",
    )


def field_tip(loc: tuple[int | str, ...]) -> str:
    """Return the description of the deepest config field named in a validation error's location."""
    model: type[BaseModel] | None = UserSettings
    tip = ""

    for key in loc:
        field = model.model_fields.get(key) if model and isinstance(key, str) else None
        if field is None:
            break

        tip = field.description or ""
        model = next(
            (
                t
                for t in get_args(field.annotation) or (field.annotation,)
                if isinstance(t, type) and issubclass(t, BaseModel)
            ),
            None,
        )

    return tip


def load_user_settings(config_file: Path = USER_CONFIG_FILE_PATH) -> dict | UserSettings:
    """
    Load user-level settings from user-level config file.

    Return an empty dict if the user config file is not found, else parse the config file
    and validate it. If the config is valid, return UserSettings.
    """
    raw_config = {}

    if not config_file.exists():
        return raw_config

    try:
        with open(config_file) as f:
            raw_config = yaml.safe_load(f) or {}
    except OSError as e:
        error(msg=f"Could not read config file {config_file}", tip=e.strerror or str(e))
        sys.exit(1)
    except yaml.YAMLError as e:
        error(msg=f"Invalid YAML in {config_file}", tip=str(e))
        sys.exit(1)

    try:
        return UserSettings.model_validate(raw_config)
    except ValidationError as e:
        for err in e.errors():
            path = ".".join(str(part) for part in err["loc"]) or config_file.name
            error(msg=f"{path}: {err['msg']}", tip=field_tip(err["loc"]))
        sys.exit(1)
