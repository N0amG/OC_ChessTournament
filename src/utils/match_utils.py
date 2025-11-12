"""Utilitaires pour l'appariement des matchs selon le système suisse."""

from models import Match, Player, Tournament


def pair_players_first_round(
    players: list[Player],
) -> tuple[list[Match], Player | None]:
    """Apparier les joueurs pour le premier round (aléatoire)."""
    matches: list[Match] = []
    bye_player: Player | None = None

    for index in range(0, len(players), 2):
        if index + 1 < len(players):
            match = Match(
                player1=players[index],
                player2=players[index + 1],
                score1=0.0,
                score2=0.0,
            )
            matches.append(match)
        else:
            bye_player = players[index]

    return matches, bye_player


def pair_players_by_score(
    tournament: Tournament,
) -> tuple[list[Match], Player | None]:
    """Apparier les joueurs par score (système suisse)."""
    sorted_players = sorted(
        tournament.players,
        key=lambda player_data: player_data[1],
        reverse=True,
    )

    played_pairs = get_played_pairs(tournament)

    matches: list[Match] = []
    paired: set[str] = set()

    for index, (player1, _score1) in enumerate(sorted_players):
        if player1.id in paired:
            continue

        best_opponent = None
        for inner_index in range(index + 1, len(sorted_players)):
            player2, _score2 = sorted_players[inner_index]

            if player2.id in paired:
                continue

            pair = tuple(sorted([player1.id, player2.id]))

            if pair not in played_pairs:
                best_opponent = inner_index
                break

            if best_opponent is None:
                best_opponent = inner_index

        if best_opponent is not None:
            opponent, _ = sorted_players[best_opponent]
            match = Match(
                player1=player1,
                player2=opponent,
                score1=0.0,
                score2=0.0,
            )
            matches.append(match)
            paired.add(player1.id)
            paired.add(opponent.id)

    bye_player: Player | None = None
    if len(paired) < len(sorted_players):
        for player, _score in sorted_players:
            if player.id not in paired:
                bye_player = player
                break

    return matches, bye_player


def get_played_pairs(tournament: Tournament) -> set[tuple[str, str]]:
    """Récupérer toutes les paires de joueurs déjà affrontées."""
    played_pairs: set[tuple[str, str]] = set()
    print("debug  : ", tournament.rounds[0])
    for round_obj in tournament.rounds:
        for match in round_obj.matches:
            pair = tuple(sorted([match.player1.id, match.player2.id]))
            played_pairs.add(pair)

    return played_pairs
