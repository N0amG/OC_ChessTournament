# OC Chess Tournament

Application de gestion de tournois d'échecs utilisant le système suisse.

## 📋 Description

Cette application permet de :
- Gérer les joueurs (création, liste)
- Créer et gérer des tournois d'échecs
- Organiser les rounds selon le système suisse
- Gérer automatiquement les "bye" (victoire par forfait) pour les nombres impairs de joueurs
- Sauvegarder les données en JSON

## 🏗️ Architecture

Le projet suit une **architecture en couches** avec une séparation claire des responsabilités :

```
┌─────────────────────────────────────────────────────┐
│                    Views (UI)                       │
│         Interface utilisateur (console)             │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│                   Managers                          │
│        Orchestration de la logique métier           │
└────────┬────────────────────────────────────┬───────┘
         │                                    │
┌────────▼────────────┐            ┌─────────▼────────┐
│    Controllers      │            │  Data Managers   │
│  (Business Logic)   │            │  (Persistence)   │
│                     │            │                  │
│ - Validation        │            │ - CRUD           │
│ - Algorithmes       │            │ - Conversions    │
│ - Règles métier     │            │   dict ↔ Entity  │
└─────────────────────┘            └─────────┬────────┘
                                             │
                                   ┌─────────▼────────┐
                                   │     Storage      │
                                   │   (JSON I/O)     │
                                   └──────────────────┘
```

### 📁 Structure du projet

```
OC_ChessTournament/
│
├── data/                           # Données JSON
│   ├── players.json                # Base de données des joueurs
│   └── tournaments.json            # Base de données des tournois
│
├── src/
│   ├── app.py                      # Point d'entrée de l'application
│   ├── models.py                   # Entités (Player, Match, Round, Tournament)
│   ├── views.py                    # Interface utilisateur (console)
│   │
│   ├── data_managers/              # 📦 Couche de persistance
│   │   ├── __init__.py             # Exports des managers
│   │   ├── storage.py              # Fonctions bas-niveau (load_json, save_json)
│   │   ├── player_manager.py       # CRUD Player + conversions dict↔Player
│   │   └── tournament_manager.py   # CRUD Tournament + conversions complexes
│   │
│   ├── controllers/                # 🎮 Logique métier
│   │   ├── __init__.py
│   │   ├── player.py               # Validation des joueurs
│   │   ├── match.py                # Algorithmes d'appariement
│   │   ├── round.py                # Gestion des rounds
│   │   └── tournament.py           # Validation des tournois
│   │
│   └── managers/                   # 🎯 Orchestration
│       ├── __init__.py
│       ├── menu.py                 # Gestion du menu principal
│       └── tournament.py           # Orchestration des tournois
│
└── README.md
```

## 🔄 Flux de données

### Exemple : Création d'un joueur

```
1. View (views.py)
   └─> Demande les informations à l'utilisateur
   
2. Manager (managers/menu.py)
   └─> Crée l'objet Player
   
3. Controller (controllers/player.py)
   └─> Valide les données (format ID, nom, date)
   
4. Data Manager (data_managers/player_manager.py)
   └─> Convertit Player → dict
   └─> Sauvegarde dans JSON via storage.py
```

### Exemple : Jouer un tournoi

```
1. View (views.py)
   └─> Affiche le menu et demande le nom du tournoi
   
2. Manager (managers/tournament.py)
   └─> Orchestre le flux du tournoi
   
3. Data Manager (data_managers/tournament_manager.py)
   └─> Charge le tournoi depuis JSON
   └─> Convertit dict → Tournament (avec Players, Rounds, Matches)
   
4. Controller (controllers/round.py)
   └─> Crée un nouveau round
   
5. Controller (controllers/match.py)
   └─> Génère les appariements selon le système suisse
   
6. View (views.py)
   └─> Affiche les matchs et demande les résultats
   
7. Controller (controllers/round.py)
   └─> Met à jour les scores du tournoi
   
8. Data Manager (data_managers/tournament_manager.py)
   └─> Sauvegarde le tournoi mis à jour
```

## 🎯 Séparation des responsabilités

### 1. **Views** (`views.py`)
- **Rôle** : Interface utilisateur
- **Responsabilités** :
  - Afficher les menus
  - Demander les entrées utilisateur
  - Afficher les résultats
- **Ne fait PAS** : Validation, accès aux données, logique métier

### 2. **Managers** (`managers/`)
- **Rôle** : Orchestration
- **Responsabilités** :
  - Coordonner les différentes couches
  - Gérer le flux de l'application
  - Appeler les controllers pour la validation
  - Appeler les data_managers pour la persistance
- **Ne fait PAS** : Accès direct aux données, validation détaillée

### 3. **Controllers** (`controllers/`)
- **Rôle** : Logique métier pure
- **Responsabilités** :
  - Validation des données (formats, règles métier)
  - Algorithmes (appariement Swiss, gestion des byes)
  - Règles du jeu
- **Ne fait PAS** : Accès aux données, conversion dict↔entity

### 4. **Data Managers** (`data_managers/`)
- **Rôle** : Couche de persistance
- **Responsabilités** :
  - CRUD (Create, Read, Update, Delete)
  - Conversions dict ↔ Entity
  - Interaction avec storage.py
- **Ne fait PAS** : Validation métier, logique algorithmique

### 5. **Storage** (`data_managers/storage.py`)
- **Rôle** : I/O JSON
- **Responsabilités** :
  - Lire les fichiers JSON
  - Écrire les fichiers JSON
- **Ne fait PAS** : Conversions, validation

## 🎲 Système Suisse

### Principe

1. **Premier round** : Appariement aléatoire des joueurs
2. **Rounds suivants** : Appariement par score
   - Les joueurs avec des scores similaires s'affrontent
   - Évite les rematches (deux joueurs ne se rencontrent qu'une seule fois)
3. **Système de points** :
   - Victoire : 1.0 point
   - Match nul : 0.5 point
   - Défaite : 0.0 point

### Gestion des "Bye"

Quand le nombre de joueurs est impair :
- Un joueur reçoit automatiquement un "bye" (victoire par forfait)
- Le joueur avec le score le plus bas reçoit le bye en priorité
- Un joueur ne peut recevoir qu'un seul bye par tournoi
- Le bye rapporte 1.0 point

## 🚀 Installation et utilisation

### Prérequis

- Python 3.10 ou supérieur

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/N0amG/OC_ChessTournament.git
cd OC_ChessTournament

# Aucune dépendance externe requise (utilise uniquement la bibliothèque standard)
```

### Lancement

```bash
cd src
python app.py
```

## 📝 Format des données

### Joueur (Player)

```python
@dataclass(frozen=True)
class Player:
    id: str          # Format: AB12345 (2 lettres majuscules + 5 chiffres)
    lastname: str    # Commence par une majuscule
    firstname: str   # Commence par une majuscule
    birthday: str    # Format: YYYY-MM-DD
```

### Match

```python
@dataclass
class Match:
    player1: Player
    player2: Player
    score1: float = 0.0  # Score du joueur 1 (0.0, 0.5, ou 1.0)
    score2: float = 0.0  # Score du joueur 2 (0.0, 0.5, ou 1.0)
```

### Round

```python
@dataclass
class Round:
    name: str                    # Ex: "Round 1"
    matches: list[Match]         # Liste des matchs du round
    started_at: str             # Date et heure de début
    ended_at: str = ""          # Date et heure de fin
```

### Tournament

```python
@dataclass
class Tournament:
    name: str                           # Nom unique du tournoi
    location: str                       # Lieu du tournoi
    start_date: str                     # Date de début (YYYY-MM-DD)
    end_date: str                       # Date de fin (YYYY-MM-DD)
    players: list[list]                 # [[Player, score], ...]
    rounds: list[Round]                 # Liste des rounds joués
    rounds_count: int = 4               # Nombre de rounds (défaut: 4)
    current_round: int = 1              # Round actuel
    description: str = ""               # Description optionnelle
```

## 🔧 Validation des données

### ID Joueur
- **Format** : `^[A-Z]{2}\d{5}$`
- **Exemple valide** : `AB12345`
- **Exemple invalide** : `ab123`, `ABC12345`

### Nom/Prénom
- **Règles** :
  - Commence par une majuscule
  - Contient uniquement des lettres, espaces, ou traits d'union
  - Accepte les accents
- **Exemples valides** : `Jean`, `Marie-Claire`, `O'Brien`, `Élise`
- **Exemples invalides** : `jean`, `Jean123`

### Date de naissance
- **Format** : `^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$`
- **Exemple valide** : `2000-08-09`
- **Exemple invalide** : `09/08/2000`, `2000-13-01`

### Dates de tournoi
- **Règle** : `start_date` doit être avant ou égal à `end_date`

## 📊 Exemple de données JSON

### players.json

```json
[
  {
    "id": "AB12345",
    "lastname": "Dupont",
    "firstname": "Jean",
    "birthday": "1990-05-15"
  },
  {
    "id": "CD67890",
    "lastname": "Martin",
    "firstname": "Marie",
    "birthday": "1985-08-22"
  }
]
```

### tournaments.json

```json
[
  {
    "name": "Tournoi A1",
    "location": "Paris",
    "start_date": "2025-11-01",
    "end_date": "2025-11-01",
    "description": "Premier tournoi",
    "rounds_count": 4,
    "current_round": 1,
    "players": [
      {
        "player": {
          "id": "AB12345",
          "lastname": "Dupont",
          "firstname": "Jean",
          "birthday": "1990-05-15"
        },
        "score": 0.0
      }
    ],
    "rounds": []
  }
]
```

## 🎓 Principes de conception

### Clean Architecture

1. **Dépendances unidirectionnelles** : Les couches extérieures dépendent des couches intérieures
2. **Indépendance de la base de données** : Le changement de JSON vers SQL nécessiterait uniquement de modifier `data_managers/`
3. **Testabilité** : Chaque couche peut être testée indépendamment
4. **Réutilisabilité** : Les controllers peuvent être réutilisés avec différentes sources de données

### SOLID

- **S** (Single Responsibility) : Chaque classe a une seule responsabilité
- **O** (Open/Closed) : Ouvert à l'extension, fermé à la modification
- **L** (Liskov Substitution) : Les dataclasses respectent leur contrat
- **I** (Interface Segregation) : Interfaces minimales et ciblées
- **D** (Dependency Inversion) : Les couches hautes ne dépendent pas des détails d'implémentation

## 🤝 Contribution

Ce projet est réalisé dans le cadre de la formation OpenClassrooms "Développeur d'application Python".

## 📄 Licence

Ce projet est sous licence MIT.

## 👤 Auteur

**Noam G**
- GitHub: [@N0amG](https://github.com/N0amG)

---

*Projet 4 - OpenClassrooms - Développeur d'application Python*
