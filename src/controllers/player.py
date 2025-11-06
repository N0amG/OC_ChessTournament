"""PlayerController - Logique métier pour les joueurs."""

import re

from managers import PlayerManager
from models import Player
from views import PlayerView
from views.logger_view import LoggerView


class PlayerController:
    """Controller orchestrant interactions vue/manager pour les joueurs."""

    def __init__(self, manager: PlayerManager | None = None) -> None:
        self.manager = manager or PlayerManager()
        self.view = PlayerView

    def manage_players(self) -> None:
        """Boucle de gestion des joueurs."""
        while True:
            choice = self.view.player_menu()

            if choice == "1":
                self.create_player()
            elif choice == "2":
                self.list_players()
            elif choice == "3":
                self.delete_player()
            elif choice == "0":
                break
            else:
                LoggerView.warning("Choix invalide. Veuillez réessayer.")

    def create_player(self) -> None:
        """Crée un joueur après validation."""
        player_data = self.view.prompt_new_player()
        player = Player(
            id=player_data["id"],
            lastname=player_data["lastname"],
            firstname=player_data["firstname"],
            birthday=player_data["birthday"],
        )

        is_valid, errors = self.validate_player(player)
        if is_valid:
            try:
                self.manager.save(player)
                LoggerView.success("Joueur créé/mis à jour avec succès !")
            except Exception as exc:  # pylint: disable=broad-except
                LoggerView.error(f"Échec de la sauvegarde du joueur : {exc}")
        else:
            LoggerView.error("Validation du joueur échouée.")
            for error in errors:
                LoggerView.warning(f"- {error}")

    def list_players(self) -> None:
        """Affiche la liste des joueurs."""
        players = self.manager.find_all()
        self.view.display_players(players)

    def delete_player(self) -> None:
        """Supprime un joueur identifié par son ID."""
        player_id = self.view.prompt_delete_player()
        player = self.manager.find_by_id(player_id)

        if player:
            self.manager.delete(player_id)
            LoggerView.success("Joueur supprimé avec succès !")
        else:
            LoggerView.error("Aucun joueur trouvé avec cet ID.")

    @staticmethod
    def validate_player(player: Player) -> tuple[bool, list[str]]:
        """
        Valide un objet Player complet
        :param player: Player - Le joueur à valider
        :return: tuple[bool, list[str]] - (True, []) si valide, sinon
            (False, [messages d'erreur])
        """
        errors: list[str] = []

        id_valid, id_error = PlayerController.validate_player_id(player.id)
        if not id_valid and id_error:
            errors.append(id_error)

        lastname_valid, lastname_error = PlayerController.validate_name(
            player.lastname,
            "nom",
        )
        if not lastname_valid and lastname_error:
            errors.append(lastname_error)

        firstname_valid, firstname_error = PlayerController.validate_name(
            player.firstname,
            "prénom",
        )
        if not firstname_valid and firstname_error:
            errors.append(firstname_error)

        birthday_valid, birthday_error = PlayerController.validate_birthday(
            player.birthday
        )
        if not birthday_valid and birthday_error:
            errors.append(birthday_error)

        return len(errors) == 0, errors

    @staticmethod
    def validate_player_id(player_id: str) -> tuple[bool, str | None]:
        """
        Valide le format de l'ID d'un joueur (AB12345)
        :param player_id: str - L'ID à valider
        :return: tuple[bool, str | None] - (True, None) si valide, sinon
            (False, message d'erreur)
        """
        if not re.match(r"^[A-Z]{2}\d{5}$", player_id):
            return False, "Format d'identifiant invalide. Exemple : AB12345."
        return True, None

    @staticmethod
    def validate_name(name: str, field_label: str) -> tuple[bool, str | None]:
        """
        Valide le format d'un nom (commence par majuscule)
        :param name: str - Le nom à valider
        :param field_label: str - Libellé du champ (nom/prénom)
        :return: tuple[bool, str | None] - (True, None) si valide, sinon
            (False, message d'erreur)
        """
        if not name or len(name.strip()) == 0:
            return False, f"Le {field_label} ne peut pas être vide."

        name_pattern = r"^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ\- ]*$"
        if not re.match(name_pattern, name):
            message = (
                f"Format de {field_label} invalide : doit commencer par "
                "une majuscule et ne contenir que des lettres, espaces ou "
                "tirets."
            )
            return False, message
        return True, None

    @staticmethod
    def validate_birthday(birthday: str) -> tuple[bool, str | None]:
        """
        Valide le format d'une date de naissance (YYYY-MM-DD)
        :param birthday: str - La date à valider
        :return: tuple[bool, str | None] - (True, None) si valide, sinon
            (False, message d'erreur)
        """
        date_pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
        if not re.match(date_pattern, birthday):
            return False, "Format de date de naissance invalide (YYYY-MM-DD)."
        return True, None
