from controllers import PlayerController
from controllers import TournamentController
from controllers import MatchController
from controllers import RoundController

from views import TournamentView

from models import Player, Tournament
from models import Round

from random import shuffle
from datetime import datetime


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
            elif choice == "4":
                TournamentManager.play_tournament()
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

        # Mélanger les joueurs
        shuffle(players)

        # Créer le tournoi
        try:
            rounds_count = int(tournament_data["rounds_count"])
        except ValueError:
            rounds_count = 4

        if tournament_data["start_date"] == "":
            tournament_data["start_date"] = datetime.now().strftime("%Y-%m-%d")

        if tournament_data["end_date"] == "":
            tournament_data["end_date"] = datetime.now().strftime("%Y-%m-%d")

        tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            players=[[player, 0.0] for player in players],
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

    @staticmethod
    def play_tournament():
        """Jouer un tournoi"""
        name = TournamentView.prompt_tournament_name()
        tournament_data = TournamentController.get_tournament_by_name(name)

        if not tournament_data:
            print(f"Aucun tournoi trouvé avec le nom '{name}'.")
            return

        # Convertir en objet Tournament
        tournament = TournamentController.dict_to_tournament(tournament_data)

        # Vérifier si le tournoi est terminé
        if tournament.current_round > tournament.rounds_count:
            print("Ce tournoi est déjà terminé!")
            TournamentView.display_rankings(tournament_data["players"])
            return

        while tournament.current_round <= tournament.rounds_count:
            print(f"\n{'=' * 50}")
            print(f"TOURNOI: {tournament.name}")
            print(f"Round {tournament.current_round}/{tournament.rounds_count}")
            print(f"{'=' * 50}")

            choice = TournamentView.play_tournament_menu()

            if choice == "1":
                TournamentManager.play_round(tournament)
                # Sauvegarder après chaque round
                TournamentController.create_or_update_tournament(tournament)
            elif choice == "2":
                # Afficher le classement
                TournamentView.display_rankings(
                    TournamentController.tournament_to_dict(tournament)["players"]
                )
            elif choice == "3":
                # Afficher les détails
                TournamentView.display_tournament_details(
                    TournamentController.tournament_to_dict(tournament)
                )
            elif choice == "0":
                # Sauvegarder avant de quitter
                TournamentController.create_or_update_tournament(tournament)
                break
            else:
                print("Choix invalide.")

        if tournament.current_round > tournament.rounds_count:
            print("\n" + "=" * 50)
            print("TOURNOI TERMINÉ!")
            print("=" * 50)
            TournamentView.display_rankings(
                TournamentController.tournament_to_dict(tournament)["players"]
            )

    @staticmethod
    def play_round(tournament: Tournament):
        """Jouer un round du tournoi"""

        round_num = tournament.current_round

        # Vérifier si le round existe déjà
        if len(tournament.rounds) >= round_num:
            print(f"Le round {round_num} a déjà été joué.")
            return

        # Créer le round avec les matchs
        new_round, bye_player = RoundController.create_round(tournament, round_num)

        print(f"\n{'='*50}")
        print(f"ROUND {round_num}")
        print(f"{'='*50}")

        # Afficher si un joueur a un "bye"
        if bye_player:
            print(
                f"\n {bye_player.lastname} {bye_player.firstname} "
                f"a un BYE ce round (victoire par forfait : +1 point)"
            )

        # Saisir les résultats de chaque match
        updated_matches = []
        for i, match in enumerate(new_round.matches, 1):
            player1_name = f"{match.player1.lastname} {match.player1.firstname}"
            player2_name = f"{match.player2.lastname} {match.player2.firstname}"

            print(f"\nMatch {i}: {player1_name} vs {player2_name}")

            score1, score2 = TournamentView.prompt_match_result(
                i, player1_name, player2_name
            )

            # Mettre à jour le match avec les scores
            MatchController.update_match_scores(match, score1, score2)
            updated_matches.append(match)

        # Créer le round avec les matchs mis à jour
        completed_round = Round(
            name=new_round.name,
            matches=updated_matches,
            started_at=new_round.started_at,
            ended_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        # Ajouter le round au tournoi
        tournament.rounds.append(completed_round)

        # Mettre à jour les scores du tournoi
        RoundController.update_tournament_scores(tournament, completed_round)

        # Ajouter 1 point au joueur en "bye" s'il y en a un
        if bye_player:
            for i, (player, score) in enumerate(tournament.players):
                if player.id == bye_player.id:
                    tournament.players[i][1] += 1.0
                    print(
                        f"✅ {bye_player.lastname} {bye_player.firstname} "
                        f"reçoit 1 point (bye)"
                    )
                    break

        # Passer au round suivant
        tournament.current_round += 1

        print(f"\nRound {round_num} terminé!")
