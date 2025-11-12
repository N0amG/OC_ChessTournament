# OC Chess Tournament

Application de gestion de tournois d'échecs utilisant le système suisse.

## 📋 Description

Cette application permet de :
- Gérer les joueurs avec identifiants uniques (création, liste, suppression)
- Créer et gérer des tournois d'échecs avec IDs uniques
- Organiser les rounds selon le système suisse
- Gérer automatiquement les « bye » (victoire par forfait) pour les nombres impairs de joueurs
- Sauvegarder toutes les données en JSON avec stockage optimisé (référencement par ID)
- Sélectionner les tournois par ID plutôt que par nom

## 🏗️ Architecture

L'application suit une architecture MVC allégée où chaque couche reste strictement limitée à son rôle :

```
┌─────────────────────────────┐
│           Views             │
│ Interface console Rich      │
└──────────────▲──────────────┘
               │
┌──────────────┴──────────────┐
│         Controllers         │
│ Orchestration + règles métier│
└──────────────▲──────────────┘
               │
┌──────────────┴──────────────┐
│          Managers           │
│ Persistance JSON            │
└──────────────▲──────────────┘
               │
┌──────────────┴──────────────┐
│           Models            │
│ Entités métier              │
└─────────────────────────────┘
```

- **Views** : affichage Rich et saisie utilisateur, aucun accès métier ou persistance.
- **Controllers** : coordonnent vues/managers, appliquent les règles métier (validation, système suisse, gestion des byes...).
- **Managers** : seules classes autorisées à lire/écrire dans les fichiers JSON via `storage.py`.
- **Models** : entités métiers (Player, Match, Round, Tournament) responsables de leurs conversions `to_dict`/`from_dict`.
- **Views/utils** : fonctions utilitaires partagées côté interface (`clear_screen`).

## 📁 Structure du projet

```
OC_ChessTournament/
│
├── data/
│   ├── players.json               # Données persistées des joueurs
│   └── tournaments.json           # Données persistées des tournois
│
├── src/
│   ├── app.py                     # Point d'entrée de l'application
│   │
│   ├── controllers/               # Logique métier et orchestration
│   │   ├── __init__.py
│   │   ├── main_controller.py     # Boucle principale
│   │   ├── match.py               # Gestion des matchs
│   │   ├── player.py              # Validation des joueurs
│   │   ├── round.py               # Gestion des rounds
│   │   └── tournament.py          # Gestion complète des tournois
│   │
│   ├── managers/                  # Persistance JSON
│   │   ├── __init__.py
│   │   ├── player_manager.py      # CRUD Player
│   │   ├── storage.py             # Utilitaires JSON génériques
│   │   └── tournament_manager.py  # CRUD Tournament
│   │
│   ├── models/                    # Entités métiers + sérialisation
│   │   ├── __init__.py
│   │   ├── match.py
│   │   ├── player.py
│   │   ├── round.py
│   │   └── tournament.py
│   │
│   └── views/                     # Interface console Rich
│       ├── __init__.py
│       ├── logger_view.py         # Messages standardisés
│       ├── main_view.py           # Menu principal
│       ├── player_view.py         # UI gestion des joueurs
│       ├── tournament_view.py     # UI gestion des tournois
│       └── utils.py               # clear_screen et helpers UI
│
└── README.md
```

## 🔄 Flux de données

### Création d'un joueur

```
1. PlayerView.prompt_new_player() recueille les entrées utilisateur.
2. PlayerController.create_player() construit l'entité Player et valide les champs.
3. PlayerManager.save() convertit le Player en dict et met à jour `players.json`.
4. LoggerView affiche le succès/échec dans la console.
```

### Jouer un round de tournoi

```
1. TournamentView.play_tournament_menu() récupère l'action choisie.
2. TournamentController._play_round() orchestre la création du round.
3. RoundController.create_round() génère les matchs via MatchController.
4. TournamentView.prompt_match_result() demande les scores, LoggerView affiche les statuts.
5. RoundController.update_tournament_scores() met à jour les scores joueurs.
6. TournamentManager.save() persiste l'état du tournoi dans `tournaments.json`.
```

## 🎯 Séparation des responsabilités

### Views (`src/views/`)
- Affichent les menus Rich, les tableaux et les résultats.
- Demandent les entrées utilisateur et les renvoient aux controllers.
- Utilisent `LoggerView` pour les messages standardisés.
- N'accèdent jamais aux fichiers ou à la logique métier.

### Controllers (`src/controllers/`)
- Coordonnent les vues et les managers.
- Appliquent la validation (formats, règles métier, dates...).
- Implémentent le système suisse et la gestion des rounds.
- Ne manipulent pas directement les fichiers JSON.

### Managers (`src/managers/`)
- Assurent le CRUD sur les fichiers JSON.
- Utilisent les méthodes `to_dict`/`from_dict` fournies par les modèles.
- Ne contiennent pas de logique d'affichage ou de validation métier.

### Models (`src/models/`)
- Représentent les entités métier.
- Fournissent `to_dict` et `from_dict` pour encapsuler la sérialisation.
- Sont utilisés par les managers, controllers et vues (pour l'affichage).

### Utils (`src/views/utils.py`)
- Fonctions utilitaires spécifiques à l'interface console (`clear_screen`).

## 🎲 Système Suisse

1. **Premier round** : appariement aléatoire des joueurs.
2. **Rounds suivants** : appariement par score (les meilleurs s'affrontent).
3. **Rematches évités** : MatchController garde les paires déjà jouées.
4. **Gestion des « bye »** : un joueur est automatiquement qualifié si le nombre de participants est impair et reçoit 1 point.

## 🆕 Fonctionnalités récentes

### Identifiants uniques pour les tournois
- Chaque tournoi possède un **ID unique** au format `AB12345` (2 lettres + 5 chiffres)
- Les tournois sont maintenant sélectionnés par **ID** plutôt que par nom
- L'ID est le **premier attribut** dans les données JSON
- Validation stricte du format d'ID lors de la création

### Stockage optimisé des joueurs
- Les joueurs ne sont plus dupliqués dans chaque tournoi et match
- Seul l'**ID du joueur** est stocké (`player_id`, `player1_id`, `player2_id`)
- Les objets `Player` sont récupérés automatiquement depuis `players.json` lors du chargement
- **Réduction de ~60%** de la taille des fichiers de tournois
- Cohérence garantie : modifier un joueur met à jour tous les tournois

### Interface améliorée
- Sélection des tournois via un tableau numéroté (pas besoin de saisir l'ID)
- Affichage de l'ID dans toutes les listes et détails de tournois
- Messages d'erreur plus clairs lors de la validation

## 🚀 Installation et utilisation

### Prérequis

- Python 3.10 ou supérieur

### Installation

```powershell
# Cloner le dépôt

cd OC_ChessTournament

# Créer l'environnement virtuel (Windows)
python -m venv .venv

# Activer l'environnement virtuel
.\.venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### Lancement

```powershell
python src/app.py
```

Sortir de l'application : saisir `0` dans le menu principal.

### Qualité de code

```powershell
# Analyse Flake8
python -m flake8 src

# Rapport HTML
python -m flake8 src --format=html --htmldir=flake8-report
start .\flake8-report\index.html
```

### Désactivation de l'environnement virtuel

```powershell
deactivate
```


## 🔧 Validation des données

- **ID joueur** : regex `^[A-Z]{2}\d{5}$` (ex: AB12345)
- **ID tournoi** : regex `^[A-Z]{2}\d{5}$` (ex: AA10000) - même format que les joueurs
- **Nom / prénom** : première lettre majuscule, lettres/espaces/traits d'union, accents autorisés
- **Date de naissance** : format `YYYY-MM-DD`
- **Dates tournoi** : `end_date` ≥ `start_date`

## � Optimisation du stockage

Pour réduire la taille des fichiers et éviter la duplication des données :
- Les **joueurs** sont stockés une seule fois dans `players.json`
- Les **tournois** référencent les joueurs par leur **ID uniquement**
- Les **matchs** utilisent également les IDs (`player1_id`, `player2_id`)

**Avantages** :
- ✅ Réduction de ~60% de la taille des fichiers de tournois
- ✅ Une seule source de vérité pour les informations des joueurs
- ✅ Modifications d'un joueur automatiquement reflétées partout
- ✅ Architecture normalisée (comme une base de données relationnelle)

## Exemples de données JSON

### players.json

```json
[
  {
    "id": "AB12345",
    "lastname": "Doe",
    "firstname": "John",
    "birthday": "1990-01-01"
  }
]
```

### tournaments.json

```json
[
  {
    "id": "AA10000",
    "name": "Tournoi A1",
    "location": "Paris",
    "start_date": "2025-11-01",
    "end_date": "2025-11-01",
    "description": "Premier tournoi",
    "rounds_count": 4,
    "current_round": 1,
    "players": [
      {
        "player_id": "AB12345",
        "score": 2.5
      }
    ],
    "rounds": [
      {
        "name": "Round 1",
        "matches": [
          {
            "player1_id": "AB12345",
            "player2_id": "CD67890",
            "score1": 1.0,
            "score2": 0.0
          }
        ],
        "started_at": "2025-11-01 14:00:00",
        "ended_at": "2025-11-01 14:30:00"
      }
    ]
  }
]
```

> **Note** : Les objets `Player` sont automatiquement récupérés via `PlayerManager.find_by_id()` lors du chargement des tournois.

## 🤝 Contribution

Projet réalisé dans le cadre de la formation OpenClassrooms « Développeur d'application Python ».

## 📄 Licence

MIT License.

## 👤 Auteur

**Noam G**  
GitHub : [@N0amG](https://github.com/N0amG)