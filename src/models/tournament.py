"""Modèle représentant un tournoi d'échecs."""

from typing import Any, Self
from .round import Round


class Tournament:
    """Structure complète d'un tournoi."""

    def __init__(
        self,
        id: str,
        name: str,
        location: str,
        start_date: str,
        end_date: str,
        players: list[list[Any]],
        rounds: list[Round],
        rounds_count: int = 4,
        current_round: int = 1,
        description: str = "",
    ) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.players = players
        self.rounds = rounds
        self.rounds_count = rounds_count
        self.current_round = current_round
        self.description = description

    def to_dict(self) -> dict[str, Any]:
        """Convertit le tournoi en dictionnaire JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "players": [
                {
                    "player_id": player.id,
                    "score": score,
                }
                for player, score in self.players
            ],
            "rounds": [round_obj.to_dict() for round_obj in self.rounds],
            "rounds_count": self.rounds_count,
            "current_round": self.current_round,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Reconstruit un tournoi depuis un dictionnaire."""
        from managers import PlayerManager

        player_manager = PlayerManager()
        players: list[list[Any]] = []

        for entry in data.get("players", []):

            player = player_manager.find_by_id(entry["player_id"])
            if not player:
                raise ValueError(
                    f"Joueur {entry['player_id']} introuvable"
                )
            score = float(entry.get("score", 0.0))
            players.append([player, score])

        rounds = [Round.from_dict(raw) for raw in data.get("rounds", [])]

        return cls(
            id=data["id"],
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            players=players,
            rounds=rounds,
            rounds_count=int(data.get("rounds_count", 4)),
            current_round=int(data.get("current_round", 1)),
            description=data.get("description", ""),
        )
