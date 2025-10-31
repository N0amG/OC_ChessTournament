"""
TournamentManager - Gère la persistance des tournois.
Responsable de : CRUD + conversions dict ↔ Tournament/Round/Match
"""

from data_managers.storage import load_json, save_json
from models import Tournament, Round, Match, Player


TOURNAMENTS_PATH = "../data/tournaments.json"


class TournamentManager:
    """Gestionnaire de données pour les tournois"""

    @staticmethod
    def save(tournament: Tournament) -> bool:
        """
        Sauvegarde un tournoi dans le stockage
        :param tournament: Tournament - Le tournoi à sauvegarder
        :return: bool - True si succès, False sinon
        """
        data = load_json(TOURNAMENTS_PATH, default=[])

        # Supprimer le tournoi existant avec le même nom
        data = [t for t in data if t["name"] != tournament.name]

        # Ajouter le tournoi
        data.append(TournamentManager._to_dict(tournament))

        save_json(TOURNAMENTS_PATH, data)
        return True

    @staticmethod
    def find_all() -> list[Tournament]:
        """
        Récupère tous les tournois
        :return: list[Tournament] - Liste de tous les tournois
        """
        data = load_json(TOURNAMENTS_PATH, default=[])
        return [TournamentManager._from_dict(t) for t in data]

    @staticmethod
    def find_by_name(name: str) -> Tournament | None:
        """
        Trouve un tournoi par son nom
        :param name: str - Le nom du tournoi
        :return: Tournament | None - Le tournoi trouvé ou None
        """
        data = load_json(TOURNAMENTS_PATH, default=[])
        for t in data:
            if t["name"] == name:
                return TournamentManager._from_dict(t)
        return None

    @staticmethod
    def delete(name: str) -> None:
        """
        Supprime un tournoi par son nom
        :param name: str - Le nom du tournoi à supprimer
        """
        data = load_json(TOURNAMENTS_PATH, default=[])
        data = [t for t in data if t["name"] != name]
        save_json(TOURNAMENTS_PATH, data)

    # ===== Méthodes de conversion privées =====

    @staticmethod
    def _to_dict(tournament: Tournament) -> dict:
        """Convertit Tournament → dict"""
        return {
            "name": tournament.name,
            "location": tournament.location,
            "start_date": tournament.start_date,
            "end_date": tournament.end_date,
            "players": [
                {
                    "player": TournamentManager._player_to_dict(p[0]),
                    "score": p[1],
                }
                for p in tournament.players
            ],
            "rounds": [
                TournamentManager._round_to_dict(r) for r in tournament.rounds
            ],
            "rounds_count": tournament.rounds_count,
            "current_round": tournament.current_round,
            "description": tournament.description,
        }

    @staticmethod
    def _from_dict(data: dict) -> Tournament:
        """Convertit dict → Tournament"""
        players_data = data.get("players", [])
        players = []

        for p_data in players_data:
            player = TournamentManager._player_from_dict(p_data["player"])
            score = p_data.get("score", 0.0)
            players.append([player, score])

        rounds = [
            TournamentManager._round_from_dict(r)
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
    def _round_to_dict(round_obj: Round) -> dict:
        """Convertit Round → dict"""
        return {
            "name": round_obj.name,
            "matches": [
                TournamentManager._match_to_dict(m) for m in round_obj.matches
            ],
            "started_at": round_obj.started_at,
            "ended_at": round_obj.ended_at,
        }

    @staticmethod
    def _round_from_dict(data: dict) -> Round:
        """Convertit dict → Round"""
        matches = [
            TournamentManager._match_from_dict(m)
            for m in data.get("matches", [])
        ]

        return Round(
            name=data["name"],
            matches=matches,
            started_at=data.get("started_at"),
            ended_at=data.get("ended_at"),
        )

    @staticmethod
    def _match_to_dict(match: Match) -> dict:
        """Convertit Match → dict"""
        return {
            "player1": TournamentManager._player_to_dict(match.player1),
            "player2": TournamentManager._player_to_dict(match.player2),
            "score1": match.score1,
            "score2": match.score2,
        }

    @staticmethod
    def _match_from_dict(data: dict) -> Match:
        """Convertit dict → Match"""
        player1 = TournamentManager._player_from_dict(data["player1"])
        player2 = TournamentManager._player_from_dict(data["player2"])

        return Match(
            player1=player1,
            player2=player2,
            score1=data.get("score1", 0),
            score2=data.get("score2", 0),
        )

    @staticmethod
    def _player_to_dict(player: Player) -> dict:
        """Convertit Player → dict"""
        return {
            "id": player.id,
            "lastname": player.lastname,
            "firstname": player.firstname,
            "birthday": player.birthday,
        }

    @staticmethod
    def _player_from_dict(data: dict) -> Player:
        """Convertit dict → Player"""
        return Player(
            id=data["id"],
            lastname=data["lastname"],
            firstname=data["firstname"],
            birthday=data["birthday"],
        )
