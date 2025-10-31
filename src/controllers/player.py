"""
PlayerController - Logique métier et validation des joueurs.
Responsable de : Validation des données joueur.
"""

import re

from models import Player


class PlayerController:
    """Controller pour la logique métier des joueurs"""

    @staticmethod
    def validate_player(player: Player) -> bool:
        """
        Valide un objet Player complet
        :param player: Player - Le joueur à valider
        :return: bool - True si valide, False sinon
        """
        return (
            PlayerController.validate_player_id(player.id)
            and PlayerController.validate_name(player.lastname)
            and PlayerController.validate_name(player.firstname)
            and PlayerController.validate_birthday(player.birthday)
        )

    @staticmethod
    def validate_player_id(player_id: str) -> bool:
        """
        Valide le format de l'ID d'un joueur (AB12345)
        :param player_id: str - L'ID à valider
        :return: bool - True si valide, False sinon
        """
        if not re.match(r"^[A-Z]{2}\d{5}$", player_id):
            print("Invalid player id format. Expected: AB12345")
            return False
        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Valide le format d'un nom (commence par majuscule)
        :param name: str - Le nom à valider
        :return: bool - True si valide, False sinon
        """
        if not name or len(name.strip()) == 0:
            print("Invalid name format: name cannot be empty.")
            return False
        
        name_pattern = r"^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ\- ]*$"
        if not re.match(name_pattern, name):
            print(
                "Invalid name format: must start with uppercase letter "
                "and contain only letters, spaces, or hyphens."
            )
            return False
        return True

    @staticmethod
    def validate_birthday(birthday: str) -> bool:
        """
        Valide le format d'une date de naissance (YYYY-MM-DD)
        :param birthday: str - La date à valider
        :return: bool - True si valide, False sinon
        """
        date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
        if not re.match(date_pattern, birthday):
            print("Invalid birthday format. Expected: YYYY-MM-DD")
            return False
        return True
