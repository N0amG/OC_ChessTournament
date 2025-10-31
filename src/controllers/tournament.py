"""
TournamentController - Logique métier et validation des tournois.
Responsable de : Validation des données tournoi.
"""

import re
from datetime import datetime

from models import Tournament


class TournamentController:
    """Controller pour la logique métier des tournois"""

    @staticmethod
    def validate_tournament(tournament: Tournament) -> bool:
        """
        Valide un objet Tournament complet
        :param tournament: Tournament - Le tournoi à valider
        :return: bool - True si valide, False sinon
        """
        # Vérifier les champs requis
        if not tournament.name or not tournament.location:
            print("Name and location cannot be empty.")
            return False

        # Valider les dates
        if not TournamentController.validate_dates(
            tournament.start_date, tournament.end_date
        ):
            return False

        # Valider les joueurs
        if not TournamentController.validate_players(tournament.players):
            return False

        return True

    @staticmethod
    def validate_dates(start_date: str, end_date: str) -> bool:
        """
        Valide les dates d'un tournoi
        :param start_date: str - Date de début (YYYY-MM-DD)
        :param end_date: str - Date de fin (YYYY-MM-DD)
        :return: bool - True si valide, False sinon
        """
        date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"

        # Vérifier le format de la date de début
        if start_date and not re.match(date_regex, start_date):
            print("Invalid start_date format. Expected: YYYY-MM-DD")
            return False

        # Vérifier le format de la date de fin
        if end_date and not re.match(date_regex, end_date):
            print("Invalid end_date format. Expected: YYYY-MM-DD")
            return False

        # Vérifier que end_date >= start_date
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if end < start:
                    print("End date must be after or equal to start date.")
                    return False
            except ValueError:
                print("Invalid date values.")
                return False

        return True

    @staticmethod
    def validate_players(players: list[list]) -> bool:
        """
        Valide la liste des joueurs d'un tournoi
        :param players: list - Liste des joueurs [Player, score]
        :return: bool - True si valide, False sinon
        """
        if len(players) < 2:
            print("Tournament must have at least 2 players.")
            return False

        return True
