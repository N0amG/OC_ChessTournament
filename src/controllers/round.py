from datetime import datetime
from models import Player, Round, Tournament
from .match import MatchController


class RoundController:
    """Controller pour gérer les rounds."""

    def __init__(
        self,
        match_controller: MatchController | None = None,
    ) -> None:
        self.match_controller = match_controller or MatchController()

    def create_round(
        self, tournament: Tournament, round_num: int
    ) -> tuple[Round, Player | None]:
        """Créer un round et générer les matchs associés."""
        bye_player: Player | None = None

        if round_num == 1:
            players_list = [
                player_data[0] for player_data in tournament.players
            ]
            matches, bye_player = (
                self.match_controller.pair_players_first_round(players_list)
            )
        else:
            matches, bye_player = self.match_controller.pair_players_by_score(
                tournament
            )

        new_round = Round(
            name=f"Round {round_num}",
            matches=matches,
            started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ended_at=None,
        )

        return new_round, bye_player

    def end_round(self, round_obj: Round) -> Round:
        """Enregistrer l'heure de fin d'un round."""
        round_obj.ended_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return round_obj

    def update_tournament_scores(
        self, tournament: Tournament, round_obj: Round
    ) -> None:
        """Mettre à jour les scores des joueurs après un round."""
        for match in round_obj.matches:
            for index, (player, _score) in enumerate(tournament.players):
                if player.id == match.player1.id:
                    tournament.players[index][1] += match.score1
                elif player.id == match.player2.id:
                    tournament.players[index][1] += match.score2
