"""Modèle représentant un tour de tournoi."""

from typing import Any, Self

from .match import Match


class Round:
    """Regroupe les matchs joués pendant un tour."""

    def __init__(
        self,
        name: str,
        matches: list[Match],
        started_at: str | None = None,
        ended_at: str | None = None,
    ) -> None:
        self.name = name
        self.matches = matches
        self.started_at = started_at
        self.ended_at = ended_at

    def to_dict(self) -> dict[str, Any]:
        """Convertit le tour en dictionnaire JSON."""
        return {
            "name": self.name,
            "matches": [match.to_dict() for match in self.matches],
            "started_at": self.started_at,
            "ended_at": self.ended_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Reconstruit un tour depuis un dictionnaire."""
        matches = [Match.from_dict(raw) for raw in data.get("matches", [])]
        return cls(
            name=data["name"],
            matches=matches,
            started_at=data.get("started_at"),
            ended_at=data.get("ended_at"),
        )
