from rich.console import Console

from ..theme import RICH_THEME


def out(msg: str, style: str | None = None) -> None:
    """Print stdout to the console using Rich."""
    console = Console(theme=RICH_THEME)
    console.print(msg, style=style)


def error(msg: str, tip: str = "") -> None:
    """Print stderr to the console using Rich."""
    console = Console(theme=RICH_THEME, stderr=True)
    console.print(f"[error]Error:[/error] {msg}")

    if tip:
        console.print(f"  ↳ {tip}", style="muted")


def warn(msg: str) -> None:
    """Print a warning to the console using Rich."""
    console = Console(theme=RICH_THEME, stderr=True)
    console.print(f"[warn]Warning:[/warn] {msg}")


def success(msg: str) -> None:
    """Print a success message to the console using Rich."""
    console = Console(theme=RICH_THEME)
    console.print(f"[success]✔[/success] {msg}")
