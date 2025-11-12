"""Modèle représentant un match d'échecs."""

from typing import Any

from .player import Player


class Match:
    """Opposition entre deux joueurs avec leurs scores."""

    def __init__(
        self,
        player1: Player,
        player2: Player,
        score1: float = 0.0,
        score2: float = 0.0,
    ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_dict(self) -> dict[str, Any]:
        """Convertit le match en dictionnaire JSON."""
        return {
            "player1_id": self.player1.id,
            "player2_id": self.player2.id,
            "score1": self.score1,
            "score2": self.score2,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Match":
        """Reconstruit un match depuis un dictionnaire."""
        from managers import PlayerManager

        player_manager = PlayerManager()

        # Support ancien format (avec objets player complets)
        if "player1" in data:
            player1 = Player(**data["player1"])
            player2 = Player(**data["player2"])
        # Nouveau format (avec IDs uniquement)
        else:
            player1 = player_manager.find_by_id(data["player1_id"])
            player2 = player_manager.find_by_id(data["player2_id"])

            if not player1 or not player2:
                raise ValueError("Joueur introuvable dans la base de données")

        return cls(
            player1=player1,
            player2=player2,
            score1=data.get("score1", 0.0),
            score2=data.get("score2", 0.0),
        )
