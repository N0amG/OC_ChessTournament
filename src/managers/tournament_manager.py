"""TournamentManager - Gestion de la persistance des tournois."""

from models import Tournament
from utils import load_json, save_json


TOURNAMENTS_PATH = "data/tournaments.json"


class TournamentManager:
    """Gestionnaire de stockage des tournois."""

    def __init__(self, storage_path: str = TOURNAMENTS_PATH) -> None:
        self.storage_path = storage_path

    def save(self, tournament: Tournament) -> bool:
        """Sauvegarde ou met à jour un tournoi."""
        data = load_json(self.storage_path, default=[])
        data = [entry for entry in data if entry["id"] != tournament.id]
        data.append(tournament.to_dict())
        save_json(self.storage_path, data)
        return True

    def find_all(self) -> list[Tournament]:
        """Retourne l'ensemble des tournois persistés."""
        data = load_json(self.storage_path, default=[])
        return [Tournament.from_dict(entry) for entry in data]

    def find_by_id(self, tournament_id: str) -> Tournament | None:
        """Recherche un tournoi par son identifiant."""
        data = load_json(self.storage_path, default=[])
        for entry in data:
            if entry["id"] == tournament_id:
                return Tournament.from_dict(entry)
        return None

    def delete(self, tournament_id: str) -> None:
        """Supprime un tournoi identifié par son identifiant."""
        data = load_json(self.storage_path, default=[])
        data = [entry for entry in data if entry["id"] != tournament_id]
        save_json(self.storage_path, data)

    # Les méthodes de conversion sont désormais gérées par les modèles.
