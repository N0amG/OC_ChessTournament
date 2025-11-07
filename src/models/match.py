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
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2,
        }
