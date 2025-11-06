"""
PlayerManager - Gestion des opérations de persistance des joueurs.
"""

from models import Player
from .storage import load_json, save_json


PLAYERS_PATH = "data/players.json"


class PlayerManager:
    """Gestionnaire de données pour les joueurs."""

    def __init__(self, storage_path: str = PLAYERS_PATH) -> None:
        self.storage_path = storage_path

    def save(self, player: Player) -> None:
        """Sauvegarde un joueur dans le stockage."""
        data = load_json(self.storage_path, default=[])
        data = [p for p in data if p["id"] != player.id]
        data.append(player.to_dict())
        save_json(self.storage_path, data)

    def find_all(self) -> list[Player]:
        """Retourne tous les joueurs persistés."""
        data = load_json(self.storage_path, default=[])
        return [Player.from_dict(p) for p in data]

    def find_by_id(self, player_id: str) -> Player | None:
        """Recherche un joueur par identifiant."""
        data = load_json(self.storage_path, default=[])
        for player_dict in data:
            if player_dict["id"] == player_id:
                return Player.from_dict(player_dict)
        return None

    def delete(self, player_id: str) -> None:
        """Supprime un joueur grâce à son identifiant."""
        data = load_json(self.storage_path, default=[])
        data = [p for p in data if p["id"] != player_id]
        save_json(self.storage_path, data)
