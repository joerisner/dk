from rich.console import Console
from rich.theme import Theme

theme = Theme({'error': 'bold red', 'success': 'bold green', 'warn': 'yellow', 'highlight': 'bold magenta'})


def out(str, style=None):
    """Print stdout to the console using Rich."""
    console = Console(theme=theme)
    console.print(str, style=style)


def error(str):
    """Print stderr to the console using Rich."""
    console = Console(theme=theme, stderr=True)
    console.print(f'[error]Error:[/error] {str}')
