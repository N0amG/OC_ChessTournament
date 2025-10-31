import re
from datetime import datetime

from controllers import PlayerController
from models import Tournament, Round, Match, Player
from storage import load_json, save_json


TOURNAMENTS_PATH = "../data/tournaments.json"


class TournamentController:

    @staticmethod
    def create_or_update_tournament(tournament: Tournament) -> bool:
        """
        Create or update a tournament in the storage \n
        :param tournament: Tournament - The tournament to create or update
        :return: bool - True if successful, False otherwise
        """
        if not TournamentController.is_tournament_valid(
            TournamentController.tournament_to_dict(tournament)
        ):
            return False

        data = load_json(TOURNAMENTS_PATH, default=[])

        # Remove existing tournament with same name if exists
        data = [t for t in data if t["name"] != tournament.name]
        data.append(TournamentController.tournament_to_dict(tournament))

        save_json(TOURNAMENTS_PATH, data)
        return True

    @staticmethod
    def delete_tournament(tournament_name: str) -> None:
        """Delete a tournament by its name"""
        data = load_json(TOURNAMENTS_PATH, default=[])
        data = [t for t in data if t["name"] != tournament_name]
        save_json(TOURNAMENTS_PATH, data)

    @staticmethod
    def get_all_tournaments() -> list:
        """Get all tournaments from storage"""
        return load_json(TOURNAMENTS_PATH, default=[])

    @staticmethod
    def get_tournament_by_name(name: str) -> dict | None:
        """Get a specific tournament by its name"""
        tournaments = load_json(TOURNAMENTS_PATH, default=[])
        for tournament in tournaments:
            if tournament["name"] == name:
                return tournament
        return None

    @staticmethod
    def tournament_to_dict(tournament: Tournament) -> dict:
        """Convert Tournament object to dictionary"""

        return {
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "players": [
                {
                    "player": PlayerController.player_to_dict(p[0]),
                    "score": p[1]
                }
                for p in tournament.players
            ],
            "rounds": [
                TournamentController.round_to_dict(r)
                for r in tournament.rounds
            ],
            "rounds_count": tournament.rounds_count,
            "current_round": tournament.current_round,
            "description": tournament.description,
        }

    @staticmethod
    def round_to_dict(round_obj: Round) -> dict:
        """Convert Round object to dictionary"""
        return {
            "name": round_obj.name,
            "matches": [
                TournamentController.match_to_dict(m)
                for m in round_obj.matches
            ],
            "started_at": round_obj.started_at,
            "ended_at": round_obj.ended_at,
        }

    @staticmethod
    def match_to_dict(match: Match) -> dict:
        """Convert Match object to dictionary"""
        return {
            "player1": PlayerController.player_to_dict(match.player1),
            "player2": PlayerController.player_to_dict(match.player2),
            "score1": match.score1,
            "score2": match.score2,
        }

    @staticmethod
    def dict_to_tournament(data: dict) -> Tournament:
        """Convert dictionary to Tournament object"""
        # Handle both old and new format for player storage
        players_data = data.get("players", [])
        players = []

        for p_data in players_data:
            # Format: {"player": {...}, "score": 0.0}
            player = Player(
                id=p_data["player"]["id"],
                lastname=p_data["player"]["lastname"],
                firstname=p_data["player"]["firstname"],
                birthday=p_data["player"]["birthday"],
            )
            score = p_data.get("score", 0.0)
            players.append([player, score])

        rounds = [
            TournamentController.dict_to_round(r)
            for r in data.get("rounds", [])
        ]
        return Tournament(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            players=players,
            rounds=rounds,
            rounds_count=data.get("rounds_count", 4),
            current_round=data.get("current_round", 1),
            description=data.get("description", ""),
        )

    @staticmethod
    def dict_to_round(data: dict) -> Round:
        """Convert dictionary to Round object"""
        matches = [
            TournamentController.dict_to_match(m)
            for m in data.get("matches", [])
        ]

        return Round(
            name=data["name"],
            matches=matches,
            started_at=data.get("started_at"),
            ended_at=data.get("ended_at"),
        )

    @staticmethod
    def dict_to_match(data: dict) -> Match:
        """Convert dictionary to Match object"""
        player1 = Player(
            id=data["player1"]["id"],
            lastname=data["player1"]["lastname"],
            firstname=data["player1"]["firstname"],
            birthday=data["player1"]["birthday"],
        )
        player2 = Player(
            id=data["player2"]["id"],
            lastname=data["player2"]["lastname"],
            firstname=data["player2"]["firstname"],
            birthday=data["player2"]["birthday"],
        )

        return Match(
            player1=player1,
            player2=player2,
            score1=data.get("score1", 0),
            score2=data.get("score2", 0),
        )

    @staticmethod
    def is_tournament_valid(tournament_data: dict) -> bool:
        """Validate tournament data"""
        required_fields = {
            "name",
            "location",
            "start_date",
            "end_date",
            "players",
            "rounds",
        }
        if not required_fields.issubset(tournament_data.keys()):
            print("Missing required fields.")
            return False

        # Validate name and location are not empty
        if not tournament_data["name"] or not tournament_data["location"]:
            print("Name and location cannot be empty.")
            return False

        # Validate date format
        date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
        if not re.match(date_regex, tournament_data["start_date"]):
            if (tournament_data["start_date"] != ""):
                print("Invalid start_date format.")
                return False
            tournament_data["start_date"] = datetime.now().strftime("%Y-%m-%d")

        if not re.match(date_regex, tournament_data["end_date"]):
            if (tournament_data["end_date"] != ""):
                print("Invalid end_date format.")
                return False
            tournament_data["end_date"] = datetime.now().strftime("%Y-%m-%d")

        # Validate end_date is after start_date
        try:
            start = datetime.strptime(
                tournament_data["start_date"], "%Y-%m-%d"
            )
            end = datetime.strptime(
                tournament_data["end_date"], "%Y-%m-%d"
            )
            if end < start:
                print(end - start)
                print("End date must be after start date.")
                return False
        except ValueError:
            print("Invalid date values.")
            return False

        # Validate players list (should have at least 2 players)
        if len(tournament_data["players"]) < 2:
            print("Tournament must have at least 2 players.")
            return False

        return True
