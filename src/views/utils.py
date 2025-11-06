"""Utilitaires partagés pour les vues."""

import os


def clear_screen() -> None:
    """Efface l'écran de manière compatible multi-plateforme."""
    os.system("cls" if os.name == "nt" else "clear")
