from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from models import Player


console = Console()


class PlayerView:

    @staticmethod
    def player_menu() -> str:
        """Menu de gestion des joueurs avec Rich"""
        console.print()
        menu_content = """
[bold white]1[/bold white]  Créer un joueur
[bold white]2[/bold white]  Lister les joueurs
[bold white]3[/bold white]  Supprimer un joueur
[bold white]0[/bold white]  Retour au menu principal
"""
        panel = Panel(
            menu_content.strip(),
            title="[bold yellow]👥 Gestion des joueurs[/bold yellow]",
            border_style="yellow",
            padding=(1, 2),
        )
        console.print(panel)
        choice = Prompt.ask(
            "[bold yellow]>[/bold yellow]",
            default="",
        ).strip()
        return choice

    @staticmethod
    def prompt_new_player() -> dict:
        """Demande les informations d'un nouveau joueur"""
        console.print(
            "\n[bold yellow]➕ Nouveau joueur[/bold yellow]", style="bold"
        )
        return {
            "id": Prompt.ask("[cyan]ID (ex: AB12345)[/cyan]").strip(),
            "lastname": Prompt.ask("[cyan]Nom[/cyan]").strip(),
            "firstname": Prompt.ask("[cyan]Prénom[/cyan]").strip(),
            "birthday": Prompt.ask(
                "[cyan]Date de naissance (YYYY-MM-DD)[/cyan]"
            ).strip(),
        }

    @staticmethod
    def prompt_delete_player() -> str:
        """Demande l'ID d'un joueur à supprimer"""
        console.print(
            "\n[bold red]➖ Supprimer un joueur[/bold red]", style="bold"
        )
        return Prompt.ask("[cyan]ID du joueur à supprimer[/cyan]").strip()

    @staticmethod
    def display_players(players: list[Player]) -> None:
        """Affiche la liste des joueurs dans un tableau Rich"""
        console.print()
        if not players:
            console.print("[yellow]ℹ Aucun joueur enregistré.[/yellow]")
            return

        table = Table(
            title="[bold yellow]📋 Liste des joueurs[/bold yellow]",
            show_header=True,
            header_style="bold cyan",
            border_style="yellow",
            title_style="bold yellow",
        )

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Nom", style="white")
        table.add_column("Prénom", style="white")
        table.add_column("Date de naissance", style="dim")

        for player in players:
            table.add_row(
                player.id, player.lastname, player.firstname, player.birthday
            )

        console.print(table)
