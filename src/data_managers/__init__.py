"""
Data Managers - Couche d'accès aux données.
Responsable de la persistance et des conversions dict ↔ entités.
"""

from data_managers.player_manager import PlayerManager
from data_managers.tournament_manager import TournamentManager

__all__ = ["PlayerManager", "TournamentManager"]
