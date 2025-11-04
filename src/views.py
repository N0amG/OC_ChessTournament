import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from models import Player, Tournament

# Instance globale de console Rich
console = Console()


def clear_screen() -> None:
    """Clear l'écran de manière compatible multi-plateforme"""
    os.system("cls" if os.name == "nt" else "clear")


def main_menu() -> str:
    """Affiche le menu principal avec Rich"""
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
    return Prompt.ask("[bold cyan]>[/bold cyan]", default="").strip()


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
        return Prompt.ask("[bold yellow]>[/bold yellow]", default="").strip()

    @staticmethod
    def prompt_new_player() -> str:
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


class TournamentView:

    @staticmethod
    def tournament_menu() -> str:
        """Menu de gestion des tournois avec Rich"""
        console.print()
        menu_content = """
[bold white]1[/bold white]  Créer un tournoi
[bold white]2[/bold white]  Lister les tournois
[bold white]3[/bold white]  Afficher un tournoi
[bold white]4[/bold white]  Jouer un tournoi
[bold white]0[/bold white]  Retour au menu principal
"""
        panel = Panel(
            menu_content.strip(),
            title="[bold green]🏆 Gestion des tournois[/bold green]",
            border_style="green",
            padding=(1, 2),
        )
        console.print(panel)
        return Prompt.ask("[bold green]>[/bold green]", default="").strip()

    @staticmethod
    def prompt_new_tournament() -> dict:
        """Demande les informations d'un nouveau tournoi"""
        console.print("\n[bold green]➕ Nouveau tournoi[/bold green]")

        name = Prompt.ask("[cyan]Nom du tournoi[/cyan]").strip()
        location = Prompt.ask("[cyan]Lieu[/cyan]").strip()
        start_date = Prompt.ask(
            "[cyan]Date de début (YYYY-MM-DD)[/cyan]",
            default=datetime.now().strftime("%Y-%m-%d"),
        ).strip()
        end_date = Prompt.ask(
            "[cyan]Date de fin (YYYY-MM-DD)[/cyan]",
            default=datetime.now().strftime("%Y-%m-%d"),
        ).strip()
        description = Prompt.ask(
            "[cyan]Description (optionnel)[/cyan]", default=""
        ).strip()
        rounds_count = Prompt.ask(
            "[cyan]Nombre de tours[/cyan]", default="4"
        ).strip()

        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
            "rounds_count": rounds_count,
        }

    @staticmethod
    def display_tournaments(tournaments: list[Tournament]) -> None:
        """Affiche la liste des tournois dans un tableau Rich"""
        console.print()
        if not tournaments:
            console.print("[yellow]ℹ Aucun tournoi enregistré.[/yellow]")
            return

        table = Table(
            title="[bold green]🏆 Liste des tournois[/bold green]",
            show_header=True,
            header_style="bold cyan",
            border_style="green",
            title_style="bold green",
        )

        table.add_column("Nom", style="white bold", no_wrap=True)
        table.add_column("Lieu", style="cyan")
        table.add_column("Date de début", style="dim")
        table.add_column("Date de fin", style="dim")
        table.add_column("Statut", style="yellow")

        for tournament in tournaments:
            # Déterminer le statut
            if tournament.current_round > tournament.rounds_count:
                status = "[green]✓ Terminé[/green]"
            else:
                status = "[yellow]En cours ({}/{})[/yellow]".format(
                    tournament.current_round,
                    tournament.rounds_count,
                )

            table.add_row(
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                status,
            )

        console.print(table)

    @staticmethod
    def display_tournament_details(tournament: Tournament) -> None:
        """Affiche les détails d'un tournoi avec un Tree Rich"""
        console.print()

        # Créer l'arbre du tournoi
        tree = Tree(
            f"[bold green]🏆 {tournament.name}[/bold green]",
            guide_style="dim cyan",
        )

        # Informations générales
        info_branch = tree.add("[bold cyan]📋 Informations[/bold cyan]")
        info_branch.add("[white]Lieu:[/white] {}".format(tournament.location))
        info_branch.add(
            "[white]Date:[/white] {} au {}".format(
                tournament.start_date,
                tournament.end_date,
            )
        )
        info_branch.add(
            "[white]Description:[/white] {}".format(
                tournament.description or "N/A"
            )
        )

        # Progression
        progress_text = f"{tournament.current_round}/{tournament.rounds_count}"
        if tournament.current_round > tournament.rounds_count:
            progress_text += " [green]✓ Terminé[/green]"
        else:
            progress_text += " [yellow]⏳ En cours[/yellow]"
        info_branch.add(f"[white]Progression:[/white] {progress_text}")

        # Joueurs
        players_branch = tree.add(
            "[bold cyan]👥 Joueurs ({})[/bold cyan]".format(
                len(tournament.players)
            )
        )

        # Trier les joueurs par score pour l'affichage
        sorted_players = sorted(
            tournament.players,
            key=lambda player_data: player_data[1],
            reverse=True,
        )
        for player, score in sorted_players[:5]:  # Afficher top 5
            players_branch.add(
                (
                    f"[white]{player.lastname} {player.firstname}[/white]"
                    f" - [yellow]{score} pts[/yellow]"
                )
            )
        if len(tournament.players) > 5:
            extra_count = len(tournament.players) - 5
            players_branch.add(f"[dim]... et {extra_count} autres[/dim]")

        # Rounds
        rounds_branch = tree.add(
            "[bold cyan]🎯 Rounds ({}/{})[/bold cyan]".format(
                len(tournament.rounds),
                tournament.rounds_count,
            )
        )
        for round_obj in tournament.rounds:
            round_info = f"[white]{round_obj.name}[/white] [green]✓[/green]"
            round_branch = rounds_branch.add(round_info)
            round_branch.add(f"[dim]Début: {round_obj.started_at}[/dim]")
            if round_obj.ended_at:
                round_branch.add(f"[dim]Fin: {round_obj.ended_at}[/dim]")
            round_branch.add(f"[dim]{len(round_obj.matches)} matchs[/dim]")

        console.print(tree)

    @staticmethod
    def prompt_tournament_name() -> str:
        """Demande le nom d'un tournoi"""
        console.print()
        return Prompt.ask("[cyan]Nom du tournoi[/cyan]").strip()

    @staticmethod
    def prompt_select_players(available_players: list[Player]) -> list[str]:
        """Sélection des joueurs avec tableau Rich"""
        console.print()
        console.print("[bold cyan]👥 Sélection des joueurs[/bold cyan]\n")

        # Afficher le tableau des joueurs disponibles
        table = Table(
            show_header=True, header_style="bold cyan", border_style="cyan"
        )

        table.add_column("N°", style="yellow", justify="center")
        table.add_column("ID", style="cyan")
        table.add_column("Nom", style="white")
        table.add_column("Prénom", style="white")

        for i, player in enumerate(available_players, 1):
            table.add_row(str(i), player.id, player.lastname, player.firstname)

        console.print(table)
        console.print()

        selection_prompt = (
            "[cyan]Entrez les numéros des joueurs séparés par des virgules "
            "(ex: 1,3,5,7)[/cyan]"
        )
        selection = Prompt.ask(selection_prompt).strip()

        selected_ids = []
        for num in selection.split(","):
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_players):
                    selected_ids.append(available_players[idx].id)
            except ValueError:
                continue

        return selected_ids

    @staticmethod
    def display_round_matches(round_obj: dict, round_num: int) -> None:
        """Afficher les matchs d'un round"""
        print(f"\n{'='*50}")
        print(f"ROUND {round_num}")
        print(f"{'='*50}")

        matches = round_obj.get("matches", [])
        if not matches:
            print("Aucun match dans ce round.")
            return

        for i, match in enumerate(matches, 1):
            player1 = match["player1"]
            player2 = match["player2"]
            score1 = match.get("score1", 0.0)
            score2 = match.get("score2", 0.0)

            print(f"\nMatch {i}:")
            print(
                f"  {player1['lastname']} {player1['firstname']} "
                f"({score1}) vs "
                f"{player2['lastname']} {player2['firstname']} ({score2})"
            )

    @staticmethod
    def prompt_match_result(
        match_num: int, player1_name: str, player2_name: str
    ) -> tuple[float, float]:
        """Demander le résultat d'un match avec Rich"""
        console.print()

        match_lines = [
            (
                f"[white]{player1_name}[/white]  [bold yellow]VS[/bold yellow]"
                f"  [white]{player2_name}[/white]"
            ),
            (
                "[bold white]1[/bold white]  Victoire "
                f"[green]{player1_name}[/green]  "
                "[dim](1.0 - 0.0)[/dim]"
            ),
            (
                "[bold white]2[/bold white]  Victoire "
                f"[green]{player2_name}[/green]  "
                "[dim](0.0 - 1.0)[/dim]"
            ),
            "[bold white]3[/bold white]  Match nul  [dim](0.5 - 0.5)[/dim]",
        ]
        match_content = "\n\n".join(match_lines)

        panel = Panel(
            match_content.strip(),
            title=f"[bold cyan]⚔️  Match {match_num}[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
        console.print(panel)

        choice = Prompt.ask(
            "[cyan]Résultat[/cyan]", choices=["1", "2", "3"], default="3"
        )

        if choice == "1":
            return (1.0, 0.0)
        elif choice == "2":
            return (0.0, 1.0)
        else:
            return (0.5, 0.5)

    @staticmethod
    def display_rankings(players_data: list[list]) -> None:
        """Afficher le classement des joueurs avec tableau Rich et médailles

        Args:
            players_data: Liste de [Player, score]
        """
        console.print()

        # Trier par score décroissant
        sorted_players = sorted(
            players_data,
            key=lambda player_data: player_data[1],
            reverse=True,
        )

        table = Table(
            title="[bold yellow]🏆 CLASSEMENT[/bold yellow]",
            show_header=True,
            header_style="bold cyan",
            border_style="yellow",
            title_style="bold yellow",
        )

        table.add_column("Rang", justify="center", style="white bold", width=6)
        table.add_column("Joueur", style="white")
        table.add_column("Score", justify="center", style="yellow bold")
        table.add_column("🏅", justify="center", width=4)

        medals = ["🥇", "🥈", "🥉"]

        for i, (player, score) in enumerate(sorted_players, 1):
            medal = medals[i - 1] if i <= 3 else ""
            rank_style = "bold gold1" if i == 1 else "bold" if i <= 3 else ""

            table.add_row(
                f"[{rank_style}]{i}[/{rank_style}]" if rank_style else str(i),
                f"{player.lastname} {player.firstname}",
                f"{score} pts",
                medal,
            )

        console.print(table)

    @staticmethod
    def play_tournament_menu() -> str:
        """Menu pour jouer un tournoi avec Rich"""
        console.print()
        menu_content = "[bold white]1[/bold white]  Jouer le prochain round\n"
        menu_content += "[bold white]2[/bold white]  Voir le classement\n"
        menu_content += (
            "[bold white]3[/bold white]  Voir les details du tournoi\n"
        )
        menu_content += "[bold white]0[/bold white]  Retour"

        panel = Panel(
            menu_content,
            title="[bold magenta]Options[/bold magenta]",
            border_style="magenta",
            padding=(1, 2),
        )
        console.print(panel)
        return Prompt.ask("[bold magenta]>[/bold magenta]", default="").strip()

    @staticmethod
    def confirm_action(message: str) -> bool:
        """Demander confirmation pour une action avec Rich"""
        response = (
            Prompt.ask(
                f"[yellow]{message}[/yellow]", choices=["o", "n"], default="n"
            )
            .strip()
            .lower()
        )
        return response == "o"
