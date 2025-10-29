from models import Player, Tournament, Round, Match
from storage import load_json, save_json
from views import PlayerView, TournamentView, main_menu
import re
from datetime import datetime


PLAYERS_PATH = "data/players.json"
TOURNAMENTS_PATH = "data/tournaments.json"


class PlayerController:

    @staticmethod
    def create_or_update_player(player) -> bool:
        """
        Create or update a player in the storage \n
        :param player: Player - The player to create or update
        :return: bool - True if the player was created or updated, False
        otherwise
        """
        if not PlayerController.is_player_valid(
            PlayerController.player_to_dict(player)
        ):
            return False

        data = load_json(PLAYERS_PATH, default=[])

        # Remove existing player with same id if exists
        data = [p for p in data if p["id"] != player.id]

        data.append(PlayerController.player_to_dict(player))

        save_json(PLAYERS_PATH, data)
        return True

    @staticmethod
    def delete_player(player_id: str) -> None:
        data = load_json(PLAYERS_PATH, default=[])

        data = [p for p in data if p["id"] != player_id]

        save_json(PLAYERS_PATH, data)

    @staticmethod
    def player_to_dict(player: Player) -> dict:
        return {
            "id": player.id,
            "lastname": player.lastname,
            "firstname": player.firstname,
            "birthday": player.birthday,
        }

    @staticmethod
    def get_all_players() -> dict:
        return load_json(PLAYERS_PATH, default={})

    @staticmethod
    def is_player_valid(player_data: dict) -> bool:
        required_fields = {"id", "lastname", "firstname", "birthday"}
        if not required_fields.issubset(player_data.keys()) and all(
            player_data.values()
        ):
            print("Missing or empty required fields.")
            return False

        if not re.match(r"^[A-Z]{2}\d{5}$", player_data["id"]):
            print("Invalid player id format.")
            return False

        name_regex = r"^[A-ZÀ-ÖØ-Þ][A-Za-zÀ-ÖØ-öø-ÿ\- ]+$"
        if not re.match(name_regex, player_data["lastname"]) or not re.match(
            name_regex, player_data["firstname"]
        ):
            print("Invalid name format.")
            return False

        if not re.match(
            r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$",
            player_data["birthday"]
        ):
            print("Invalid birthday format.")
            return False

        return True


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
                PlayerController.player_to_dict(p) for p in tournament.players
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
        players = [
            Player(
                id=p["id"],
                lastname=p["lastname"],
                firstname=p["firstname"],
                birthday=p["birthday"],
            )
            for p in data.get("players", [])
        ]

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
            print("Invalid start_date format.")
            return False
        if not re.match(date_regex, tournament_data["end_date"]):
            print("Invalid end_date format.")
            return False

        # Validate end_date is after start_date
        try:
            start = datetime.strptime(
                tournament_data["start_date"], "%Y-%m-%d"
            )
            end = datetime.strptime(tournament_data["end_date"], "%Y-%m-%d")
            if end < start:
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


class TournamentManager:
    """Manager pour gérer les interactions avec les tournois"""

    @staticmethod
    def run():
        """Lance le gestionnaire de tournois"""
        while True:
            choice = TournamentView.tournament_menu()

            if choice == "1":
                TournamentManager.create_tournament()
            elif choice == "2":
                TournamentManager.list_tournaments()
            elif choice == "3":
                TournamentManager.show_tournament_details()
            elif choice == "0":
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

    @staticmethod
    def create_tournament():
        """Créer un nouveau tournoi"""
        tournament_data = TournamentView.prompt_new_tournament()

        # Charger tous les joueurs disponibles
        all_players = PlayerController.get_all_players()
        if len(all_players) < 2:
            print(
                "Erreur : Il faut au moins 2 joueurs enregistrés "
                "pour créer un tournoi."
            )
            return

        # Sélectionner les joueurs
        selected_ids = TournamentView.prompt_select_players(all_players)
        if len(selected_ids) < 2:
            print(
                "Erreur : Vous devez sélectionner au moins 2 joueurs "
                "pour le tournoi."
            )
            return

        # Créer les objets Player
        players = [
            Player(
                id=p["id"],
                lastname=p["lastname"],
                firstname=p["firstname"],
                birthday=p["birthday"],
            )
            for p in all_players
            if p["id"] in selected_ids
        ]

        # Créer le tournoi
        try:
            rounds_count = int(tournament_data["rounds_count"])
        except ValueError:
            rounds_count = 4

        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            players=players,
            rounds=[],
            rounds_count=rounds_count,
            current_round=1,
            description=tournament_data["description"],
        )

        if TournamentController.create_or_update_tournament(tournament):
            print("Tournoi créé avec succès !")
        else:
            print("Erreur lors de la création du tournoi.")

    @staticmethod
    def list_tournaments():
        """Lister tous les tournois"""
        tournaments = TournamentController.get_all_tournaments()
        TournamentView.display_tournaments(tournaments)

    @staticmethod
    def show_tournament_details():
        """Afficher les détails d'un tournoi"""
        name = TournamentView.prompt_tournament_name()
        tournament = TournamentController.get_tournament_by_name(name)

        if tournament:
            TournamentView.display_tournament_details(tournament)
        else:
            print(f"Aucun tournoi trouvé avec le nom '{name}'.")


class MenuManager:
    @staticmethod
    def menu_controller():

        while True:
            choice = main_menu()
            if choice == "1":
                player_data = PlayerView.prompt_new_player()
                player = Player(
                    id=player_data["id"],
                    lastname=player_data["lastname"],
                    firstname=player_data["firstname"],
                    birthday=player_data["birthday"],
                )
                if PlayerController.create_or_update_player(player):
                    print("Player created/updated successfully.")
                else:
                    print("Failed to create/update player.")
            elif choice == "2":
                players = PlayerController.get_all_players()
                PlayerView.display_players(players)
            elif choice == "3":
                TournamentManager.run()
            elif choice == "0":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    MenuManager.menu_controller()
