def main_menu() -> str:
    print("\n=== OC Chess Tournaments ===")
    print("1) Créer un joueur")
    print("2) Lister les joueurs")
    print("0) Quitter")
    return input("> ").strip()


class PlayerView:

    @staticmethod
    def prompt_new_player() -> str:
        print("\n-- Nouveau joueur --")
        return {
            "id": input("ID : ").strip(),
            "lastname": input("Nom : ").strip(),
            "firstname": input("Prénom : ").strip(),
            "birthday": input("Date de naissance (YYYY-MM-DD) : ").strip(),
        }

    @staticmethod
    def display_players(players: list[dict]) -> None:
        print("\n-- Liste des joueurs --")
        if not players:
            print("Aucun joueur enregistré.")
            return

        for player in players:
            print(
                f"{player['id']} - {player['lastname']} "
                f"{player['firstname']} - {player['birthday']}"
            )


if __name__ == "__main__":
    prompt = main_menu()
    print(f"You selected option: {prompt}")
    liste = [
        {
            "id": "AB12345",
            "lastname": "Dupont",
            "firstname": "Jean",
            "birthday": "1990-01-01",
        },
        {
            "id": "XY99999",
            "lastname": "Le Grand",
            "firstname": "Jean-Luc",
            "birthday": "2000-12-31",
        },
        {
            "id": "AZ00001",
            "lastname": "Évrard",
            "firstname": "Élodie",
            "birthday": "1985-05-09",
        },
        {
            "id": "BC54321",
            "lastname": "De La Tour",
            "firstname": "Anne Marie",
            "birthday": "1970-07-15",
        },
    ]
    PlayerView.display_players(liste)
    if prompt == "1":
        new_player = PlayerView.prompt_new_player()
        print(f"Joueur {new_player['lastname']} {new_player['firstname']} créé !")
