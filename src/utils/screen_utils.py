"""Utilitaires pour l'interface console."""

import os


def clear_screen() -> None:
    """Efface l'écran de manière compatible multi-plateforme."""
    os.system("cls" if os.name == "nt" else "clear")
