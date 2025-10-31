from datetime import datetime

from controllers import MatchController
from models import Tournament, Round, Player


class RoundController:
    """Controller pour gérer les rounds"""

    @staticmethod
    def create_round(
        tournament: Tournament, round_num: int
    ) -> tuple[Round, Player | None]:
        """
        Créer un nouveau round avec les matchs appropriés \n
        :param tournament: Tournament - Le tournoi
        :param round_num: int - Le numéro du round
        :return: tuple[Round, Player | None] - Le round créé et le joueur
        en "bye" si nombre impair
        """
        bye_player = None

        # Créer les paires de joueurs
        if round_num == 1:
            # Premier round : appariement aléatoire
            players_list = [p[0] for p in tournament.players]
            matches, bye_player = MatchController.pair_players_first_round(
                players_list
            )
        else:
            # Rounds suivants : appariement par score
            matches, bye_player = MatchController.pair_players_by_score(
                tournament
            )

        # Créer le round avec l'heure de début
        new_round = Round(
            name=f"Round {round_num}",
            matches=matches,
            started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ended_at=None,
        )

        return new_round, bye_player

    @staticmethod
    def end_round(round_obj: Round) -> Round:
        """
        Terminer un round en enregistrant l'heure de fin \n
        :param round_obj: Round - Le round à terminer
        :return: Round - Le round avec l'heure de fin
        """
        return Round(
            name=round_obj.name,
            matches=round_obj.matches,
            started_at=round_obj.started_at,
            ended_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    @staticmethod
    def update_tournament_scores(tournament: Tournament, round_obj: Round):
        """
        Mettre à jour les scores des joueurs dans le tournoi après un round
        :param tournament: Tournament - Le tournoi
        :param round_obj: Round - Le round terminé
        """
        for match in round_obj.matches:
            # Trouver et mettre à jour le score de chaque joueur
            for i, (player, score) in enumerate(tournament.players):
                if player.id == match.player1.id:
                    tournament.players[i][1] += match.score1
                elif player.id == match.player2.id:
                    tournament.players[i][1] += match.score2
