from datetime import datetime


def main_menu() -> str:
    print("\n=== OC Chess Tournaments ===")
    print("1) Gérer les joueurs")
    print("2) Gérer les tournois")
    print("0) Quitter")
    return input("> ").strip()


class PlayerView:

    @staticmethod
    def player_menu() -> str:
        print("\n=== Gestion des joueurs ===")
        print("1) Créer un joueur")
        print("2) Lister les joueurs")
        print("0) Retour au menu principal")
        return input("> ").strip()

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
        print("4) Jouer un tournoi")
        print("0) Retour au menu principal")
        return input("> ").strip()

    @staticmethod
    def prompt_new_tournament() -> dict:
        print("\n-- Nouveau tournoi --")
        return {
            "name": input("Nom du tournoi : ").strip(),
            "location": input("Lieu : ").strip(),
            "start_date": input("Date de début (YYYY-MM-DD) : ").strip()
            or datetime.now().strftime("%Y-%m-%d"),
            "end_date": input("Date de fin (YYYY-MM-DD) : ").strip()
            or datetime.now().strftime("%Y-%m-%d"),
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

        # Afficher les joueurs avec leur score
        players_data = tournament.get("players", [])
        print(f"Nombre de joueurs : {len(players_data)}")

        if players_data:
            print("\nJoueurs inscrits :")
            for p_data in players_data:
                # Format: {"player": {...}, "score": 0.0}
                player = p_data["player"]
                score = p_data.get("score", 0.0)
                print(
                    f"  - {player['lastname']} {player['firstname']} "
                    f"(Score: {score})"
                )

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

    @staticmethod
    def display_round_matches(round_obj: dict, round_num: int) -> None:
        """Afficher les matchs d'un round"""
        print(f"\n{'='*50}")
        print(f"ROUND {round_num}")
        print(f"{'='*50}")

        matches = round_obj.get("matches", [])
        if not matches:
            print("Aucun match dans ce round.")
            return

        for i, match in enumerate(matches, 1):
            player1 = match["player1"]
            player2 = match["player2"]
            score1 = match.get("score1", 0.0)
            score2 = match.get("score2", 0.0)

            print(f"\nMatch {i}:")
            print(
                f"  {player1['lastname']} {player1['firstname']} "
                f"({score1}) vs "
                f"{player2['lastname']} {player2['firstname']} ({score2})"
            )

    @staticmethod
    def prompt_match_result(
        match_num: int, player1_name: str, player2_name: str
    ) -> tuple[float, float]:
        """Demander le résultat d'un match"""
        print(f"\n--- Résultat du Match {match_num} ---")
        print(f"1) {player1_name} gagne (1.0 - 0.0)")
        print(f"2) {player2_name} gagne (0.0 - 1.0)")
        print("3) Match nul (0.5 - 0.5)")

        choice = input("Résultat > ").strip()

        if choice == "1":
            return (1.0, 0.0)
        elif choice == "2":
            return (0.0, 1.0)
        elif choice == "3":
            return (0.5, 0.5)
        else:
            print("Choix invalide. Match nul par défaut.")
            return (0.5, 0.5)

    @staticmethod
    def display_rankings(players_data: list[dict]) -> None:
        """Afficher le classement des joueurs"""
        print("\n" + "=" * 50)
        print("CLASSEMENT")
        print("=" * 50)

        # Trier par score décroissant
        sorted_players = sorted(
            players_data, key=lambda x: x.get("score", 0.0), reverse=True
        )

        for i, p_data in enumerate(sorted_players, 1):
            # Format: {"player": {...}, "score": 0.0}
            player = p_data["player"]
            score = p_data.get("score", 0.0)
            print(
                f"{i}. {player['lastname']} {player['firstname']} "
                f"- {score} points"
            )

    @staticmethod
    def play_tournament_menu() -> str:
        """Menu pour jouer un tournoi"""
        print("\n--- Options ---")
        print("1) Jouer le prochain round")
        print("2) Voir le classement")
        print("3) Voir les détails du tournoi")
        print("0) Retour")
        return input("> ").strip()

    @staticmethod
    def confirm_action(message: str) -> bool:
        """Demander confirmation pour une action"""
        response = input(f"{message} (o/n) : ").strip().lower()
        return response in ["o", "oui", "y", "yes"]
