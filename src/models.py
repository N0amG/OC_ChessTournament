from dataclasses import dataclass


# ---- Player Model ---- #


@dataclass
class Player:
    """
    This class define a player \n
    :param id: str - The player's unique identifier
    :param lastname: str - The player's last name
    :param firstname: str - The player's first name
    :param birthday: str - The player's birthday in YYYY-MM-DD format
    """

    id: str
    lastname: str
    firstname: str
    birthday: str

# ---- Match Model ---- #


@dataclass
class Match:
    """
    This class define a match between two players \n
    :param player1: Player - The first player
    :param player2: Player - The second player
    :param score1: float - The score of the first player
    :param score2: float - The score of the second player
    """

    player1: Player
    player2: Player
    score1: float = 0
    score2: float = 0


# ---- Round Model ---- #


@dataclass
class Round:
    """
    This class define a round in a tournament \n
    :param name: str - The name of the round
    :param matches: list[Match] - The list of matches in the round
    :param started_at: str - The start time of the round
    :param ended_at: str - The end time of the round
    """

    name: str
    matches: list[Match]

    # Both optionnal
    started_at: str = None
    ended_at: str = None


# ---- Tournament Model ---- #


@dataclass
class Tournament:
    """
    This class define a tournament \n
    :param name: str - The name of the tournament
    :param location: str - The location of the tournament
    :param start_date: str - The start date of the tournament in YYYY-MM-DD
    format
    :param end_date: str - The end date of the tournament in YYYY-MM-DD format
    """

    name: str
    location: str
    start_date: str  # format YYYY-MM-DD
    end_date: str  # format YYYY-MM-DD
    players: list[list[Player, int]]  # List of [Player, score in tournament]
    rounds: list[Round]
    rounds_count: int = 4
    current_round: int = 1
    description: str = ""
