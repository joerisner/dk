from enum import StrEnum

import rich_click as click
from rich.theme import Theme


class Styles(StrEnum):
    """Output styles matching rich-click's `cargo` color palette."""

    error = "bold red"
    success = "bold green"
    warn = "bold yellow"
    highlight = "bold cyan"
    muted = "dim white"


# Theme for rich output.
RICH_THEME = Theme({s.name: s.value for s in Styles})


# rich-click help settings.
RICH_CLICK_HELP_CONFIG = click.RichHelpConfiguration(
    theme="cargo-slim",
    ##############
    ## Behavior ##
    ##############
    enable_theme_env_var=False,
    commands_before_options=True,
    use_rich_markup=True,
    ##############
    ### Options ##
    ##############
    options_table_column_types=["opt_all_metavar", "help"],
    ##############
    ### Errors ###
    ##############
    style_errors_panel_box="BLANK",
    errors_panel_title="Error:",
    errors_suggestion=False,  # type: ignore - False is a valid value.
    padding_errors_panel=(0,),
    ##############
    ### Aborted ##
    ##############
    aborted_text="Aborted",
    style_aborted=Styles.error,
)
