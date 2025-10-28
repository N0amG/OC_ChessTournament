from models import Player
from storage import load_json, save_json
import re


PLAYERS_PATH = "data/players.json"


class PlayerController:

    @staticmethod
    def register_player(player) -> bool:

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

        data.append(PlayerController.player_to_dict(player))

        save_json(PLAYERS_PATH, data)

    @staticmethod
    def unregister_player(player_id: str) -> None:
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
            r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", player_data["birthday"]
        ):
            print("Invalid birthday format.")
            return False

        return True


def create_player(player_data: dict) -> Player | bool:
    if not PlayerController.is_player_valid(player_data):
        return False

    player = Player(**player_data)
    player.register_player()
    return player


if __name__ == "__main__":
    player = Player(
        id="AB12345", lastname="Doe", firstname="John", birthday="1990-01-01"
    )
    PlayerController.register_player(player)