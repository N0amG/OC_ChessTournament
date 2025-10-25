import json
from dataclasses import dataclass


@dataclass
class Player:
    """This class define a player \n
    :param id: str - The player's unique identifier
    :param lastname: str - The player's last name
    :param firstname: str - The player's first name
    :param birthday: str - The player's birthday in YYYY-MM-DD format
    """

    __id: str
    __lastname: str
    __firstname: str
    __birthday: str

    @property
    def id(self):
        return self.__id

    @property
    def lastname(self):
        return self.__lastname

    @property
    def firstname(self):
        return self.__firstname

    @property
    def birthday(self):
        return self.__birthday

    def register_player(self):
        player = {
            "lastname": self.lastname,
            "firstname": self.firstname,
            "birthday": self.birthday,
            "id": self.id,
        }

        with open("data/players.json", "r") as f:
            try:
                data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

        data[player["id"]] = player

        with open("data/players.json", "w") as f:
            json.dump(data, f, indent=4)


player = Player("AB1235", "Doe", "John", "1990-01-01")
player.register_player()
print(player)
