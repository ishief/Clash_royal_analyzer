# Clash Royale Analyzer

Projet Python de récupération, parsing, stockage et visualisation de données issues de l’API officielle Clash Royale.  
Ce projet a pour objectif d’analyser un historique de batailles, de calculer quelques statistiques utiles et de générer des graphiques exportables pour un portfolio.

## Fonctionnalités

- Appel à l’API Clash Royale avec `requests`
- Chargement sécurisé de la clé API via `.env`
- Récupération d’un battlelog joueur
- Sauvegarde des données brutes en JSON
- Parsing des données utiles en CSV
- Stockage dans une base SQLite
- Calcul de statistiques simples :
  - nombre total de batailles
  - wins / losses / draws
  - winrate global
  - cartes les plus utilisées
  - winrate par deck
- Génération de graphiques en `.png`

## Structure du projet

```text
clash-royale-analyzer/
├── src/
│   ├── api.py
│   ├── parser.py
│   ├── database.py
│   ├── analysis.py
│   ├── visualisation.py
│   └── main.py
├── data/
│   ├── raw/
│   ├── processed/
│   └── royalapi.db
├── graphs/
│   ├── top_cards.png
│   ├── results_distribution.png
│   ├── winrate_by_deck.png
│   └── game_modes.png
├── notebooks/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. Cloner le dépôt :
```bash
git clone <url_du_repo>
cd clash-royale-analyzer
```

2. Créer et activer un environnement virtuel :
```bash
python -m venv .venv
```

Windows PowerShell :
```bash
.venv\Scripts\Activate.ps1
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

Créer un fichier `.env` à la racine du projet :

```env
PROJET_ROYALAPI=votre_cle_api
PLAYER_TAG=#VOTRE_TAG
```

## Utilisation

### 1. Récupérer les données et alimenter la base
```bash
python src/main.py
```

Ce script :
- appelle l’API Clash Royale,
- sauvegarde le battlelog en JSON,
- génère un CSV,
- crée et remplit la base SQLite.

### 2. Lancer les analyses
```bash
python src/analysis.py
```

### 3. Générer les graphiques
```bash
python src/visualisation.py
```

Les images sont exportées dans le dossier `graphs/`.

## Graphiques générés

- Top 10 des cartes les plus utilisées
- Répartition des résultats
- Winrate par deck
- Répartition des modes de jeu

## Sécurité et confidentialité

Ce projet utilise un fichier `.env` ignoré par Git pour éviter de publier :
- la clé API Clash Royale
- le tag du compte utilisé pour les tests

Les données brutes (`data/raw/`), la base SQLite locale et certains exports peuvent être exclus du dépôt public afin de ne pas exposer les données détaillées d’un compte tiers.

## Technologies utilisées

- Python
- Requests
- Python-dotenv
- Pandas
- SQLite
- Matplotlib
- Seaborn

## Améliorations possibles

- Anonymisation automatique des tags dans les exports
- Analyse de plusieurs joueurs
- Dashboard interactif
- Export de rapports statistiques
- Amélioration du schéma relationnel

## Auteur

Projet réalisé par ishief dans le cadre d’un apprentissage backend / data autour de Python, SQL et visualisation de données.