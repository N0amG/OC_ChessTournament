
from models import Match


class MatchController:
    """Controller pour gérer les matchs."""

    def create_match(self, player1, player2) -> Match:
        """Créer un match entre deux joueurs."""
        return Match(
            player1=player1,
            player2=player2,
            score1=0.0,
            score2=0.0,
        )

    def update_match_scores(
        self,
        match: Match,
        score1: float,
        score2: float,
    ) -> None:
        """Mettre à jour les scores d'un match."""
        match.score1 = score1
        match.score2 = score2
