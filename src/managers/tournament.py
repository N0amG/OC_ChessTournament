from datetime import datetime
from random import shuffle

from rich.console import Console

from controllers.match import MatchController
from controllers.round import RoundController
from controllers.tournament import TournamentController
from data_managers import (
    PlayerManager,
    TournamentManager as TournamentDataManager,
)
from models import Round, Tournament
from views import TournamentView

console = Console()


class TournamentManager:
    """Manager pour gérer les interactions avec les tournois"""

    @staticmethod
    def run():
        """Lance le gestionnaire de tournois"""
        while True:
            choice = TournamentView.tournament_menu()

            if choice == "1":
                TournamentManager.create_tournament()
            elif choice == "2":
                TournamentManager.list_tournaments()
            elif choice == "3":
                TournamentManager.show_tournament_details()
            elif choice == "4":
                TournamentManager.play_tournament()
            elif choice == "0":
                break
            else:
                console.print(
                    "[yellow]⚠ Choix invalide. " "Veuillez réessayer.[/yellow]"
                )

    @staticmethod
    def create_tournament():
        """Créer un nouveau tournoi"""
        tournament_data = TournamentView.prompt_new_tournament()

        # Charger tous les joueurs disponibles
        all_players = PlayerManager.find_all()
        if len(all_players) < 2:
            console.print(
                "[red]✗ Erreur : Il faut au moins 2 joueurs enregistrés "
                "pour créer un tournoi.[/red]"
            )
            return

        # Sélectionner les joueurs
        selected_ids = TournamentView.prompt_select_players(all_players)
        if len(selected_ids) < 2:
            console.print(
                "[red]✗ Erreur : Vous devez sélectionner au moins 2 "
                "joueurs pour le tournoi.[/red]"
            )
            return

        # Filtrer les joueurs sélectionnés
        players = [p for p in all_players if p.id in selected_ids]

        # Mélanger les joueurs
        shuffle(players)

        # Créer le tournoi
        try:
            rounds_count = int(tournament_data["rounds_count"])
        except ValueError:
            rounds_count = 4

        if tournament_data["start_date"] == "":
            tournament_data["start_date"] = datetime.now().strftime("%Y-%m-%d")

        if tournament_data["end_date"] == "":
            tournament_data["end_date"] = datetime.now().strftime("%Y-%m-%d")

        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            players=[[player, 0.0] for player in players],
            rounds=[],
            rounds_count=rounds_count,
            current_round=1,
            description=tournament_data["description"],
        )

        # Valider puis sauvegarder
        if TournamentController.validate_tournament(tournament):
            if TournamentDataManager.save(tournament):
                console.print("[green]✓ Tournoi créé avec succès ![/green]")
            else:
                console.print(
                    "[red]✗ Erreur lors de la sauvegarde " "du tournoi.[/red]"
                )
        else:
            console.print("[red]✗ Erreur de validation du tournoi.[/red]")

    @staticmethod
    def list_tournaments():
        """Lister tous les tournois"""
        tournaments = TournamentDataManager.find_all()
        TournamentView.display_tournaments(tournaments)

    @staticmethod
    def show_tournament_details():
        """Afficher les détails d'un tournoi"""
        name = TournamentView.prompt_tournament_name()
        tournament = TournamentDataManager.find_by_name(name)

        if tournament:
            TournamentView.display_tournament_details(tournament)
        else:
            console.print(
                f"[yellow]⚠ Aucun tournoi trouvé avec le nom "
                f"'{name}'.[/yellow]"
            )

    @staticmethod
    def play_tournament():
        """Jouer un tournoi"""
        name = TournamentView.prompt_tournament_name()
        tournament = TournamentDataManager.find_by_name(name)

        if not tournament:
            console.print(
                f"[yellow]⚠ Aucun tournoi trouvé avec le nom "
                f"'{name}'.[/yellow]"
            )
            return

        # Vérifier si le tournoi est terminé
        if tournament.current_round > tournament.rounds_count:
            console.print(
                (
                    "\n[bold yellow]🏁 Ce tournoi est déjà terminé !"
                    "[/bold yellow]\n"
                )
            )
            TournamentView.display_rankings(tournament.players)
            return

        while tournament.current_round <= tournament.rounds_count:
            console.print(f"\n[bold cyan]{'=' * 50}[/bold cyan]")
            console.print(
                f"[bold green]🏆 TOURNOI: {tournament.name}[/bold green]"
            )
            console.print(
                f"[bold yellow]Round {tournament.current_round}/"
                f"{tournament.rounds_count}[/bold yellow]"
            )
            console.print(f"[bold cyan]{'=' * 50}[/bold cyan]")

            choice = TournamentView.play_tournament_menu()

            if choice == "1":
                TournamentManager.play_round(tournament)
                # Sauvegarder après chaque round
                TournamentDataManager.save(tournament)
            elif choice == "2":
                # Afficher le classement
                TournamentView.display_rankings(tournament.players)
            elif choice == "3":
                # Afficher les détails
                TournamentView.display_tournament_details(tournament)
            elif choice == "0":
                # Sauvegarder avant de quitter
                TournamentDataManager.save(tournament)
                break
            else:
                console.print("[yellow]⚠ Choix invalide.[/yellow]")

        if tournament.current_round > tournament.rounds_count:
            console.print(f"\n[bold green]{'=' * 50}[/bold green]")
            console.print("[bold yellow]🏁 TOURNOI TERMINÉ ![/bold yellow]")
            console.print(f"[bold green]{'=' * 50}[/bold green]")
            TournamentView.display_rankings(tournament.players)

    @staticmethod
    def play_round(tournament: Tournament):
        """Jouer un round du tournoi"""

        round_num = tournament.current_round

        # Vérifier si le round existe déjà
        if len(tournament.rounds) >= round_num:
            console.print(
                f"[yellow]⚠ Le round {round_num} a déjà été joué.[/yellow]"
            )
            return

        # Créer le round avec les matchs
        new_round, bye_player = RoundController.create_round(
            tournament, round_num
        )

        console.print(f"\n[bold cyan]{'='*50}[/bold cyan]")
        console.print(f"[bold yellow]🎯 ROUND {round_num}[/bold yellow]")
        console.print(f"[bold cyan]{'='*50}[/bold cyan]")

        # Afficher si un joueur a un "bye"
        if bye_player:
            console.print(
                f"\n[yellow]⚡ {bye_player.lastname} "
                f"{bye_player.firstname} a un BYE ce round "
                f"(victoire par forfait : +1 point)[/yellow]\n"
            )

        # Saisir les résultats de chaque match
        updated_matches = []
        for i, match in enumerate(new_round.matches, 1):
            player1_name = (
                f"{match.player1.lastname} {match.player1.firstname}"
            )
            player2_name = (
                f"{match.player2.lastname} {match.player2.firstname}"
            )

            score1, score2 = TournamentView.prompt_match_result(
                i, player1_name, player2_name
            )

            # Mettre à jour le match avec les scores
            MatchController.update_match_scores(match, score1, score2)
            updated_matches.append(match)

        # Créer le round avec les matchs mis à jour
        round_with_matches = Round(
            name=new_round.name,
            matches=updated_matches,
            started_at=new_round.started_at,
            ended_at=None,
        )

        # Terminer le round en enregistrant l'heure de fin
        RoundController.end_round(round_with_matches)

        # Ajouter le round au tournoi
        tournament.rounds.append(round_with_matches)

        # Mettre à jour les scores du tournoi
        RoundController.update_tournament_scores(
            tournament, round_with_matches
        )

        # Ajouter 1 point au joueur en "bye" s'il y en a un
        if bye_player:
            for i, (player, score) in enumerate(tournament.players):
                if player.id == bye_player.id:
                    tournament.players[i][1] += 1.0
                    console.print(
                        f"[green]✓ {bye_player.lastname} "
                        f"{bye_player.firstname} "
                        f"reçoit 1 point (bye)[/green]"
                    )
                    break

        # Passer au round suivant
        tournament.current_round += 1

        console.print(
            f"\n[bold green]✓ Round {round_num} terminé ![/bold green]\n"
        )
