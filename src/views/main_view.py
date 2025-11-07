from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from utils import clear_screen

console = Console()


class MainView:
    """Vue principale pour l'accueil de l'application"""

    @staticmethod
    def main_menu() -> str:
        """Affiche le menu principal avec Rich et renvoie le choix"""

        clear_screen()

        menu_text = Text()
        menu_text.append("🏆 OC Chess Tournaments 🏆", style="bold cyan")

        menu_content = """
[bold white]1[/bold white]  Gérer les joueurs
[bold white]2[/bold white]  Gérer les tournois
[bold white]0[/bold white]  Quitter
"""

        panel = Panel(
            menu_content.strip(),
            title=menu_text,
            border_style="cyan",
            padding=(1, 2),
        )
        console.print(panel)
        choice = Prompt.ask(
            "[bold cyan]>[/bold cyan]",
            default="",
        ).strip()
        clear_screen()
        return choice

    @staticmethod
    def display_goodbye() -> None:
        console.print(
            "\n[bold cyan]👋 Au revoir ! Merci d'avoir utilisé OC Chess "
            "Tournaments.[/bold cyan]\n"
        )
