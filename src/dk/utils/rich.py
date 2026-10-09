from rich.console import Console
from rich.theme import Theme

theme = Theme(
    {
        "error": "bold red",
        "success": "bold green",
        "warn": "bold yellow",
        "highlight": "bold magenta",
        "muted": "dim white",
    }
)


def out(msg: str, style: str | None = None) -> None:
    """Print stdout to the console using Rich."""
    console = Console(theme=theme)
    console.print(msg, style=style)


def error(msg: str, tip: str = "") -> None:
    """Print stderr to the console using Rich."""
    console = Console(theme=theme, stderr=True)
    console.print(f"[error]Error:[/error] {msg}")

    if tip:
        console.print(f"  ↳ {tip}", style="muted")


def warn(msg: str) -> None:
    """Print a warning to the console using Rich."""
    console = Console(theme=theme, stderr=True)
    console.print(f"[warn]Warning:[/warn] {msg}")
