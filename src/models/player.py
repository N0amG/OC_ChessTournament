"""Modèle représentant un joueur."""

from typing import Self


class Player:
    """Informations d'identité pour un joueur."""

    def __init__(
        self,
        id: str,
        lastname: str,
        firstname: str,
        birthday: str,
    ) -> None:
        self.id = id
        self.lastname = lastname
        self.firstname = firstname
        self.birthday = birthday

    def to_dict(self) -> dict[str, str]:
        """Convertit le joueur vers un dictionnaire JSON."""
        return {
            "id": self.id,
            "lastname": self.lastname,
            "firstname": self.firstname,
            "birthday": self.birthday,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        """Reconstruit un joueur depuis un dictionnaire."""
        return cls(
            id=data["id"],
            lastname=data["lastname"],
            firstname=data["firstname"],
            birthday=data["birthday"],
        )
