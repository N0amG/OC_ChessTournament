"""TournamentController - Logique métier des tournois."""

import re
from datetime import datetime
from random import shuffle

from controllers.match import MatchController
from controllers.round import RoundController
from managers import PlayerManager, TournamentManager
from models import Round, Tournament
from views import TournamentView
from views.logger_view import LoggerView


class TournamentController:
    """Controller orchestrant vues et managers pour les tournois."""

    def __init__(
        self,
        manager: TournamentManager | None = None,
        player_manager: PlayerManager | None = None,
        match_controller: MatchController | None = None,
        round_controller: RoundController | None = None,
    ) -> None:
        self.manager = manager or TournamentManager()
        self.player_manager = player_manager or PlayerManager()
        self.match_controller = match_controller or MatchController()
        self.round_controller = (
            round_controller
            if round_controller is not None
            else RoundController(self.match_controller)
        )
        self.view = TournamentView

    def manage_tournaments(self) -> None:
        """Boucle principale de gestion des tournois."""
        while True:
            choice = self.view.tournament_menu()

            if choice == "1":
                self.create_tournament()
            elif choice == "2":
                self.list_tournaments()
            elif choice == "3":
                self.show_tournament_details()
            elif choice == "4":
                self.play_tournament()
            elif choice == "5":
                self.delete_tournament()
            elif choice == "0":
                break
            else:
                LoggerView.warning("Choix invalide. Veuillez réessayer.")

    def create_tournament(self) -> None:
        """Crée un tournoi après validation."""
        tournament_data = self.view.prompt_new_tournament()

        all_players = self.player_manager.find_all()
        if len(all_players) < 2:
            LoggerView.error(
                "Il faut au moins 2 joueurs enregistrés pour créer un tournoi."
            )
            return

        selected_ids = self.view.prompt_select_players(all_players)
        if len(selected_ids) < 2:
            LoggerView.error(
                "Vous devez sélectionner au moins 2 joueurs pour le tournoi."
            )
            return

        players = [
            player for player in all_players if player.id in selected_ids
        ]
        shuffle(players)

        try:
            rounds_count = int(tournament_data["rounds_count"])
        except ValueError:
            rounds_count = 4

        if tournament_data["start_date"] == "":
            tournament_data["start_date"] = datetime.now().strftime("%Y-%m-%d")

        if tournament_data["end_date"] == "":
            tournament_data["end_date"] = datetime.now().strftime("%Y-%m-%d")

        tournament = Tournament(
            id=tournament_data["id"],
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

        is_valid, errors = TournamentController.validate_tournament(tournament)
        if not is_valid:
            LoggerView.error("Validation du tournoi échouée.")
            for error in errors:
                LoggerView.warning(f"- {error}")
            return

        try:
            saved = self.manager.save(tournament)
        except Exception as e:
            LoggerView.error(
                f"Erreur lors de la sauvegarde du tournoi : {e}"
            )
            return

        if saved:
            LoggerView.success("Tournoi créé avec succès !")
        else:
            LoggerView.error(
                "Sauvegarde non confirmée. Veuillez réessayer."
            )

    def list_tournaments(self) -> None:
        """Affiche la liste des tournois."""
        tournaments = self.manager.find_all()
        self.view.display_tournaments(tournaments)

    def delete_tournament(self) -> None:
        """Supprime un tournoi via son identifiant."""
        tournaments = self.manager.find_all()
        tournament_id = self.view.prompt_select_tournament(tournaments)

        if not tournament_id:
            LoggerView.error("Aucun tournoi sélectionné.")
            return

        tournament = self.manager.find_by_id(tournament_id)

        if tournament:
            self.manager.delete(tournament_id)
            LoggerView.success("Tournoi supprimé avec succès !")
        else:
            LoggerView.error(
                f"Aucun tournoi trouvé avec l'ID '{tournament_id}'."
            )

    def show_tournament_details(self) -> None:
        """Affiche les détails d'un tournoi."""
        tournaments = self.manager.find_all()
        tournament_id = self.view.prompt_select_tournament(tournaments)

        if not tournament_id:
            LoggerView.error("Aucun tournoi sélectionné.")
            return

        tournament = self.manager.find_by_id(tournament_id)

        if tournament:
            self.view.display_tournament_details(tournament)
        else:
            LoggerView.error(
                f"Aucun tournoi trouvé avec l'ID '{tournament_id}'."
            )

    def play_tournament(self) -> None:
        """Gère le déroulement d'un tournoi."""
        tournaments = self.manager.find_all()
        tournament_id = self.view.prompt_select_tournament(tournaments)

        if not tournament_id:
            LoggerView.error("Aucun tournoi sélectionné.")
            return

        tournament = self.manager.find_by_id(tournament_id)

        if not tournament:
            LoggerView.error(
                f"Aucun tournoi trouvé avec l'ID '{tournament_id}'."
            )
            return

        if tournament.current_round > tournament.rounds_count:
            self.view.display_tournament_already_finished()
            self.view.display_rankings(tournament.players)
            return

        while tournament.current_round <= tournament.rounds_count:
            self.view.display_tournament_round_banner(
                tournament.name,
                tournament.current_round,
                tournament.rounds_count,
            )

            choice = self.view.play_tournament_menu()

            if choice == "1":
                self._play_round(tournament)
                self.manager.save(tournament)
            elif choice == "2":
                self.view.display_rankings(tournament.players)
            elif choice == "3":
                self.view.display_tournament_details(tournament)
            elif choice == "0":
                self.manager.save(tournament)
                break
            else:
                LoggerView.warning("Choix invalide. Veuillez réessayer.")

        if tournament.current_round > tournament.rounds_count:
            self.view.display_tournament_finished()
            self.view.display_rankings(tournament.players)

    def _play_round(self, tournament: Tournament) -> None:
        """Joue un round et met à jour le tournoi."""
        round_num = tournament.current_round

        if len(tournament.rounds) >= round_num:
            self.view.display_round_already_played(round_num)
            return

        new_round, bye_player = self.round_controller.create_round(
            tournament,
            round_num,
        )

        self.view.display_round_banner(round_num)

        if bye_player:
            self.view.display_bye_message(bye_player)

        updated_matches = []
        for index, match in enumerate(new_round.matches, 1):
            player1_name = (
                f"{match.player1.lastname} {match.player1.firstname}"
            )
            player2_name = (
                f"{match.player2.lastname} {match.player2.firstname}"
            )

            score1, score2 = self.view.prompt_match_result(
                index,
                player1_name,
                player2_name,
            )

            self.match_controller.update_match_scores(match, score1, score2)
            updated_matches.append(match)

        round_with_matches = Round(
            name=new_round.name,
            matches=updated_matches,
            started_at=new_round.started_at,
            ended_at=None,
        )

        self.round_controller.end_round(round_with_matches)
        tournament.rounds.append(round_with_matches)
        self.round_controller.update_tournament_scores(
            tournament,
            round_with_matches,
        )

        if bye_player:
            for index, (player, score) in enumerate(tournament.players):
                if player.id == bye_player.id:
                    tournament.players[index][1] += 1.0
                    self.view.display_bye_points_awarded(bye_player)
                    break

        tournament.current_round += 1
        self.view.display_round_completed(round_num)

    @staticmethod
    def validate_tournament(tournament: Tournament) -> tuple[bool, list[str]]:
        """
        Valide un objet Tournament complet
        :param tournament: Tournament - Le tournoi à valider
        :return: tuple[bool, list[str]] - (True, []) si valide, sinon
            (False, [messages d'erreur])
        """
        errors: list[str] = []

        # Valider l'ID
        id_valid, id_error = TournamentController.validate_tournament_id(
            tournament.id
        )
        if not id_valid:
            errors.append(id_error)

        # Vérifier les champs requis
        if not tournament.name or not tournament.location:
            errors.append("Le nom et le lieu du tournoi sont obligatoires.")

        # Valider les dates
        dates_valid, date_errors = TournamentController.validate_dates(
            tournament.start_date,
            tournament.end_date,
        )
        if not dates_valid:
            errors.extend(date_errors)

        # Valider les joueurs
        players_valid, player_errors = TournamentController.validate_players(
            tournament.players
        )
        if not players_valid:
            errors.extend(player_errors)

        return len(errors) == 0, errors

    @staticmethod
    def validate_tournament_id(tournament_id: str) -> tuple[bool, str | None]:
        """
        Valide le format de l'ID d'un tournoi (AB12345)
        :param tournament_id: str - L'ID à valider
        :return: tuple[bool, str | None] - (True, None) si valide, sinon
            (False, message d'erreur)
        """
        if not re.match(r"^[A-Z]{2}\d{5}$", tournament_id):
            return (
                False,
                "Format d'identifiant invalide. Exemple : AB12345.",
            )
        return True, None

    @staticmethod
    def validate_dates(
        start_date: str,
        end_date: str,
    ) -> tuple[bool, list[str]]:
        """
        Valide les dates d'un tournoi
        :param start_date: str - Date de début (YYYY-MM-DD)
        :param end_date: str - Date de fin (YYYY-MM-DD)
        :return: tuple[bool, list[str]] - (True, []) si valide, sinon
            (False, [messages d'erreur])
        """
        errors: list[str] = []
        date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

        effective_start = start_date or datetime.now().strftime("%Y-%m-%d")
        effective_end = end_date or datetime.now().strftime("%Y-%m-%d")

        # Vérifier le format de la date de début
        if start_date and not re.match(date_regex, start_date):
            errors.append(
                "Format de date de début invalide. Attendu : YYYY-MM-DD."
            )

        # Vérifier le format de la date de fin
        if end_date and not re.match(date_regex, end_date):
            errors.append(
                "Format de date de fin invalide. Attendu : YYYY-MM-DD."
            )

        # En l'absence d'erreur de format, vérifier que end_date >= start_date
        if not errors:
            try:
                start = datetime.strptime(effective_start, "%Y-%m-%d")
                end = datetime.strptime(effective_end, "%Y-%m-%d")
                if end < start:
                    errors.append(
                        "La date de fin doit être postérieure ou égale à la"
                        " date de début."
                    )
            except ValueError:
                errors.append("Valeurs de date invalides.")

        return len(errors) == 0, errors

    @staticmethod
    def validate_players(
        players: list[list],
    ) -> tuple[bool, list[str]]:
        """
        Valide la liste des joueurs d'un tournoi
        :param players: list - Liste des joueurs [Player, score]
        :return: tuple[bool, list[str]] - (True, []) si valide, sinon
            (False, [messages d'erreur])
        """
        errors: list[str] = []

        if len(players) < 2:
            errors.append("Le tournoi doit compter au moins deux joueurs.")

        return len(errors) == 0, errors
