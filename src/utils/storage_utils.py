"""Fonctions utilitaires pour la persistance JSON."""

import json
import os
from typing import Any


def load_json(path: str, default: Any) -> Any:
    """Charge un fichier JSON.

    Renvoie son contenu ou une valeur par défaut.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(path: str, data: Any) -> None:
    """Écrit des données dans un fichier JSON."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=4)
