from rich.console import Console

console = Console()


class LoggerView:
    """Affiche des messages standardisés dans la console."""

    @staticmethod
    def error(message: str) -> None:
        console.print(f"[red]✗ {message}[/red]")

    @staticmethod
    def success(message: str) -> None:
        console.print(f"[green]✓ {message}[/green]")

    @staticmethod
    def warning(message: str) -> None:
        console.print(f"[yellow]⚠ {message}[/yellow]")

    @staticmethod
    def info(message: str) -> None:
        console.print(f"[cyan]{message}[/cyan]")
