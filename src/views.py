def main_menu() -> str:
    print("\n=== OC Chess Tournaments ===")
    print("1) Créer un joueur")
    print("2) Lister les joueurs")
    print("3) Gérer les tournois")
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


class TournamentView:

    @staticmethod
    def tournament_menu() -> str:
        print("\n=== Gestion des tournois ===")
        print("1) Créer un tournoi")
        print("2) Lister les tournois")
        print("3) Afficher un tournoi")
        print("0) Retour au menu principal")
        return input("> ").strip()

    @staticmethod
    def prompt_new_tournament() -> dict:
        print("\n-- Nouveau tournoi --")
        return {
            "name": input("Nom du tournoi : ").strip(),
            "location": input("Lieu : ").strip(),
            "start_date": input("Date de début (YYYY-MM-DD) : ").strip(),
            "end_date": input("Date de fin (YYYY-MM-DD) : ").strip(),
            "description": input("Description (optionnel) : ").strip(),
            "rounds_count": input("Nombre de tours (défaut 4) : ").strip()
            or "4",
        }

    @staticmethod
    def display_tournaments(tournaments: list[dict]) -> None:
        print("\n-- Liste des tournois --")
        if not tournaments:
            print("Aucun tournoi enregistré.")
            return

        for tournament in tournaments:
            print(
                f"- {tournament['name']} | {tournament['location']} | "
                f"{tournament['start_date']} au {tournament['end_date']}"
            )

    @staticmethod
    def display_tournament_details(tournament: dict) -> None:
        print("\n=== Détails du tournoi ===")
        print(f"Nom : {tournament['name']}")
        print(f"Lieu : {tournament['location']}")
        print(f"Date : {tournament['start_date']} au {tournament['end_date']}")
        print(f"Description : {tournament.get('description', 'N/A')}")
        print(
            f"Tour actuel : {tournament['current_round']}/"
            f"{tournament['rounds_count']}"
        )
        print(f"Nombre de joueurs : {len(tournament['players'])}")
        print(f"Nombre de tours joués : {len(tournament['rounds'])}")

    @staticmethod
    def prompt_tournament_name() -> str:
        return input("\nNom du tournoi : ").strip()

    @staticmethod
    def prompt_select_players(available_players: list[dict]) -> list[str]:
        print("\n-- Sélection des joueurs --")
        print("Joueurs disponibles :")
        for i, player in enumerate(available_players, 1):
            print(
                f"{i}) {player['id']} - {player['lastname']} "
                f"{player['firstname']}"
            )

        print(
            "\nEntrez les numéros des joueurs séparés par des virgules "
            "(ex: 1,3,5,7)"
        )
        selection = input("> ").strip()

        selected_ids = []
        for num in selection.split(","):
            try:
                idx = int(num.strip()) - 1
                if 0 <= idx < len(available_players):
                    selected_ids.append(available_players[idx]["id"])
            except ValueError:
                continue

        return selected_ids
