from models import Player, Match, Tournament


class MatchController:
    """Controller pour gérer les matchs"""

    @staticmethod
    def create_match(player1: Player, player2: Player) -> Match:
        """
        Créer un nouveau match entre deux joueurs \n
        :param player1: Player - Le premier joueur
        :param player2: Player - Le deuxième joueur
        :return: Match - Le match créé
        """
        return Match(
            player1=player1,
            player2=player2,
            score1=0.0,
            score2=0.0,
        )

    @staticmethod
    def update_match_scores(match: Match, score1: float, score2: float):
        """
        Mettre à jour les scores d'un match \n
        :param match: Match - Le match à mettre à jour
        :param score1: float - Score du joueur 1 (1.0 = victoire, 0.5 = nul,
        0.0 = défaite)
        :param score2: float - Score du joueur 2
        """
        match.score1 = score1
        match.score2 = score2

    @staticmethod
    def pair_players_first_round(
        players: list[Player]
    ) -> tuple[list[Match], Player | None]:
        """
        Apparier les joueurs pour le premier round (aléatoire) \n
        :param players: list[Player] - Liste des joueurs
        :return: tuple[list[Match], Player | None] - Liste des matchs
        créés et joueur en "bye" (si nombre impair)
        """
        matches = []
        bye_player = None

        for i in range(0, len(players), 2):
            if i + 1 < len(players):
                match = MatchController.create_match(
                    players[i], players[i + 1]
                )
                matches.append(match)
            else:
                # Nombre impair : le dernier joueur a un "bye"
                bye_player = players[i]

        return matches, bye_player

    @staticmethod
    def pair_players_by_score(
        tournament: Tournament
    ) -> tuple[list[Match], Player | None]:
        """
        Apparier les joueurs par score (système suisse) \n
        :param tournament: Tournament - Le tournoi
        :return: tuple[list[Match], Player | None] - Liste des matchs
        créés et joueur en "bye" (si nombre impair)
        """
        # Trier les joueurs par score décroissant
        sorted_players = sorted(
            tournament.players, key=lambda x: x[1], reverse=True
        )

        # Récupérer les paires déjà jouées
        played_pairs = MatchController.get_played_pairs(tournament)

        matches = []
        paired = set()

        for i, (player1, score1) in enumerate(sorted_players):
            if player1.id in paired:
                continue

            best_opponent = None
            # Chercher un adversaire pas encore rencontré
            for j in range(i + 1, len(sorted_players)):
                player2, score2 = sorted_players[j]

                if player2.id in paired:
                    continue

                pair = tuple(sorted([player1.id, player2.id]))

                # Priorité 1 : adversaire jamais rencontré
                if pair not in played_pairs:
                    best_opponent = j
                    break
                # Priorité 2 : si tous ont été rencontrés,
                # prendre le premier disponible
                elif best_opponent is None:
                    best_opponent = j

            # Si un adversaire a été trouvé, créer le match
            if best_opponent is not None:
                player2, score2 = sorted_players[best_opponent]
                match = MatchController.create_match(player1, player2)
                matches.append(match)
                paired.add(player1.id)
                paired.add(player2.id)

        # Trouver le joueur en "bye" (non apparié) s'il y en a un
        bye_player = None
        if len(paired) < len(sorted_players):
            for player, score in sorted_players:
                if player.id not in paired:
                    bye_player = player
                    break

        return matches, bye_player

    @staticmethod
    def get_played_pairs(tournament: Tournament) -> set:
        """
        Récupérer toutes les paires de joueurs déjà affrontées \n
        :param tournament: Tournament - Le tournoi
        :return: set - Ensemble des paires déjà jouées
        """
        played_pairs = set()

        for round_obj in tournament.rounds:
            for match in round_obj.matches:
                pair = tuple(sorted([match.player1.id, match.player2.id]))
                played_pairs.add(pair)

        return played_pairs
