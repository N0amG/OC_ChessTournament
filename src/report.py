"""Generation de rapports CSV pour les joueurs et tournois.

Executer ce module genere automatiquement les cinq rapports demandes, tous
stockes dans ``data/reports``.
"""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence

from managers import PlayerManager, TournamentManager
from models import Tournament

REPORTS_DIR = Path("data") / "reports"


class ReportGenerator:
    """Fabrique les rapports CSV a partir des donnees persistees."""

    def __init__(
        self,
        output_dir: Path | None = None,
        run_timestamp: str | None = None,
        player_manager: PlayerManager | None = None,
        tournament_manager: TournamentManager | None = None,
    ) -> None:
        self.timestamp = run_timestamp or datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
        target_dir = output_dir or REPORTS_DIR / f"report_{self.timestamp}"
        self.output_dir = target_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.player_manager = player_manager or PlayerManager()
        self.tournament_manager = tournament_manager or TournamentManager()

    def generate_players_report(self) -> Path:
        """Genere la liste des joueurs par ordre alphabetique."""
        players = sorted(
            self.player_manager.find_all(),
            key=lambda player: (
                player.lastname.lower(),
                player.firstname.lower(),
            ),
        )
        headers = ["player_id", "lastname", "firstname", "birthday"]
        rows = [
            [player.id, player.lastname, player.firstname, player.birthday]
            for player in players
        ]
        output_path = self._timestamped_filename("joueurs_alphabetique")
        self._write_csv(output_path, headers, rows)
        return output_path

    def generate_tournaments_report(self) -> Path:
        """Genere la liste de tous les tournois."""
        tournaments = sorted(
            self.tournament_manager.find_all(),
            key=lambda tournament: (
                tournament.name.lower(),
                tournament.start_date,
            ),
        )
        headers = [
            "tournament_id",
            "name",
            "location",
            "start_date",
            "end_date",
            "rounds_count",
            "current_round",
            "players_count",
            "description",
        ]
        rows = [
            [
                tournament.id,
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                tournament.rounds_count,
                tournament.current_round,
                len(tournament.players),
                tournament.description,
            ]
            for tournament in tournaments
        ]
        output_path = self._timestamped_filename("tous_les_tournois")
        self._write_csv(output_path, headers, rows)
        return output_path

    def generate_tournament_info_report(self, tournament_id: str) -> Path:
        """Genere un rapport nom et dates pour un tournoi donne."""
        tournament = self._get_tournament_or_raise(tournament_id)
        headers = ["tournament_id", "name", "start_date", "end_date"]
        rows = [
            [
                tournament.id,
                tournament.name,
                tournament.start_date,
                tournament.end_date,
            ]
        ]
        output_path = self._timestamped_filename(
            f"{tournament.id.lower()}_dates"
        )
        self._write_csv(output_path, headers, rows)
        return output_path

    def generate_tournament_players_report(self, tournament_id: str) -> Path:
        """Genere la liste des joueurs d'un tournoi donne."""
        tournament = self._get_tournament_or_raise(tournament_id)
        players_with_scores = sorted(
            tournament.players,
            key=lambda entry: (
                entry[0].lastname.lower(),
                entry[0].firstname.lower(),
            ),
        )
        headers = [
            "tournament_id",
            "player_id",
            "lastname",
            "firstname",
            "score",
        ]
        rows = [
            [
                tournament.id,
                player.id,
                player.lastname,
                player.firstname,
                score,
            ]
            for player, score in players_with_scores
        ]
        output_path = self._timestamped_filename(
            f"{tournament.id.lower()}_joueurs"
        )
        self._write_csv(output_path, headers, rows)
        return output_path

    def generate_tournament_rounds_report(self, tournament_id: str) -> Path:
        """Genere la liste des tours et des matchs pour un tournoi donne."""
        tournament = self._get_tournament_or_raise(tournament_id)
        headers = [
            "tournament_id",
            "round_name",
            "started_at",
            "ended_at",
            "match_number",
            "player1_id",
            "player1_name",
            "score1",
            "player2_id",
            "player2_name",
            "score2",
        ]
        rows: list[list[str | float | int]] = []
        for round_obj in tournament.rounds:
            for index, match in enumerate(round_obj.matches, start=1):
                rows.append(
                    [
                        tournament.id,
                        round_obj.name,
                        round_obj.started_at or "",
                        round_obj.ended_at or "",
                        index,
                        match.player1.id,
                        (
                            f"{match.player1.firstname} "
                            f"{match.player1.lastname}"
                        ),
                        match.score1,
                        match.player2.id,
                        (
                            f"{match.player2.firstname} "
                            f"{match.player2.lastname}"
                        ),
                        match.score2,
                    ]
                )
        output_path = self._timestamped_filename(
            f"{tournament.id.lower()}_tours_matchs"
        )
        self._write_csv(output_path, headers, rows)
        return output_path

    def _timestamped_filename(self, slug: str) -> Path:
        return self.output_dir / f"{slug}_{self.timestamp}.csv"

    def _get_tournament_or_raise(self, tournament_id: str) -> Tournament:
        tournament = self.tournament_manager.find_by_id(tournament_id)
        if tournament is None:
            raise ValueError(f"Tournoi introuvable : {tournament_id}")
        return tournament

    @staticmethod
    def _write_csv(
        path: Path,
        headers: Sequence[str],
        rows: Iterable[Sequence[object]],
    ) -> None:
        with path.open("w", encoding="utf-8", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=";")
            writer.writerow(headers)
            for row in rows:
                writer.writerow(row)


def choose_tournament(tournaments: list[Tournament]) -> Tournament:
    """Invite l'utilisateur a selectionner un tournoi."""
    print("Tournois disponibles :")
    for index, tournament in enumerate(tournaments, start=1):
        print(f"{index}. {tournament.id} - {tournament.name}")
    user_choice = input("Choisissez un numero ou un ID : ").strip()
    if not user_choice:
        raise SystemExit("Selection vide. Rapport annule.")

    for tournament in tournaments:
        if user_choice.upper() == tournament.id.upper():
            return tournament
    if user_choice.isdigit():
        position = int(user_choice)
        if 1 <= position <= len(tournaments):
            return tournaments[position - 1]

    raise SystemExit("Aucun tournoi ne correspond a la selection.")


def main() -> None:
    """Genere exactement cinq rapports et affiche leur chemin."""
    generator = ReportGenerator()
    tournaments = generator.tournament_manager.find_all()
    if not tournaments:
        raise SystemExit("Aucun tournoi enregistre.")
    selected_tournament = choose_tournament(tournaments)

    reports: list[tuple[str, Path]] = []
    reports.append(("joueurs", generator.generate_players_report()))
    reports.append(("tournois", generator.generate_tournaments_report()))
    reports.append(
        (
            f"infos_{selected_tournament.id.lower()}",
            generator.generate_tournament_info_report(selected_tournament.id),
        )
    )
    reports.append(
        (
            f"joueurs_{selected_tournament.id.lower()}",
            generator.generate_tournament_players_report(
                selected_tournament.id
            ),
        )
    )
    reports.append(
        (
            f"tours_{selected_tournament.id.lower()}",
            generator.generate_tournament_rounds_report(
                selected_tournament.id
            ),
        )
    )

    for label, path in reports:
        print(f"{label} -> {path}")


if __name__ == "__main__":
    main()
