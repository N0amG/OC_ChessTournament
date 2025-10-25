from dataclasses import dataclass


@dataclass
class Tournament:
    """This class define a tournament"""

    name: str
    place: str
    start_date: str  # format YYYY-MM-DD
    end_date: str  # format YYYY-MM-DD
    rounds_number: int = 4
    current_round: int = 1
    rounds: list
    players: list
    description: str
