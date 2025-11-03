"""
PlayerManager - Gère la persistance des joueurs.
Responsable de : CRUD + conversions dict ↔ Player
"""

from data_managers.storage import load_json, save_json
from models import Player


PLAYERS_PATH = "data/players.json"


class PlayerManager:
    """Gestionnaire de données pour les joueurs"""

    @staticmethod
    def save(player: Player) -> bool:
        """
        Sauvegarde un joueur dans le stockage
        :param player: Player - Le joueur à sauvegarder
        :return: bool - True si succès, False sinon
        """
        data = load_json(PLAYERS_PATH, default=[])

        # Supprimer le joueur existant avec le même ID
        data = [p for p in data if p["id"] != player.id]

        # Ajouter le joueur
        data.append(PlayerManager._to_dict(player))

        save_json(PLAYERS_PATH, data)
        return True

    @staticmethod
    def find_all() -> list[Player]:
        """
        Récupère tous les joueurs
        :return: list[Player] - Liste de tous les joueurs
        """
        data = load_json(PLAYERS_PATH, default=[])
        return [PlayerManager._from_dict(p) for p in data]

    @staticmethod
    def find_by_id(player_id: str) -> Player | None:
        """
        Trouve un joueur par son ID
        :param player_id: str - L'ID du joueur
        :return: Player | None - Le joueur trouvé ou None
        """
        data = load_json(PLAYERS_PATH, default=[])
        for p in data:
            if p["id"] == player_id:
                return PlayerManager._from_dict(p)
        return None

    @staticmethod
    def delete(player_id: str) -> None:
        """
        Supprime un joueur par son ID
        :param player_id: str - L'ID du joueur à supprimer
        """
        data = load_json(PLAYERS_PATH, default=[])
        data = [p for p in data if p["id"] != player_id]
        save_json(PLAYERS_PATH, data)

    @staticmethod
    def _to_dict(player: Player) -> dict:
        """
        Convertit un Player en dictionnaire (privé)
        :param player: Player - Le joueur à convertir
        :return: dict - Le dictionnaire représentant le joueur
        """
        return {
            "id": player.id,
            "lastname": player.lastname,
            "firstname": player.firstname,
            "birthday": player.birthday,
        }

    @staticmethod
    def _from_dict(data: dict) -> Player:
        """
        Convertit un dictionnaire en Player (privé)
        :param data: dict - Le dictionnaire à convertir
        :return: Player - L'objet Player créé
        """
        return Player(
            id=data["id"],
            lastname=data["lastname"],
            firstname=data["firstname"],
            birthday=data["birthday"],
        )
