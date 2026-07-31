import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "data/royalapi.db"
GRAPH_DIR = "graphs"

os.makedirs(GRAPH_DIR, exist_ok=True)
sns.set_style("whitegrid")

def load_data():
    conn = sqlite3.connect(DB_PATH)
    battles = pd.read_sql_query("SELECT * FROM battles", conn)
    cards = pd.read_sql_query("SELECT * FROM battle_cards", conn)
    conn.close()
    return battles, cards

def plot_top_cards(cards):
    df = (
        cards[cards["owner"] == "player"]["card_name"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    df.columns = ["card_name", "count"]

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="count", y="card_name", hue="card_name", palette="Blues_r", legend=False)
    plt.title("Top 10 des cartes les plus utilisées")
    plt.xlabel("Nombre d'utilisations")
    plt.ylabel("Carte")
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/top_cards.png")
    plt.close()

def plot_results_distribution(battles):
    df = battles["result"].value_counts().reset_index()
    df.columns = ["result", "count"]

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="result", y="count", hue="result", palette="Set2", legend=False)
    plt.title("Répartition des résultats")
    plt.xlabel("Résultat")
    plt.ylabel("Nombre de batailles")
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/results_distribution.png")
    plt.close()

def plot_winrate_by_deck(battles):
    df = battles.groupby("player_deck").agg(
        matches=("battle_id", "count"),
        wins=("result", lambda x: (x == "win").sum())
    ).reset_index()

    df["winrate"] = (df["wins"] / df["matches"]) * 100
    df = df[df["matches"] >= 2].sort_values(by="winrate", ascending=False).head(10)

    plt.figure(figsize=(14, 7))
    sns.barplot(data=df, x="winrate", y="player_deck", hue="player_deck", palette="viridis", legend=False)
    plt.title("Winrate par deck (min. 2 matchs)")
    plt.xlabel("Winrate (%)")
    plt.ylabel("Deck")
    plt.subplots_adjust(left=0.35, right=0.95, top=0.9, bottom=0.1)
    plt.savefig(f"{GRAPH_DIR}/winrate_by_deck.png")
    plt.close()

def plot_game_modes(battles):
    df = battles["game_mode"].value_counts().reset_index()
    df.columns = ["game_mode", "count"]

    plt.figure(figsize=(10, 5))
    sns.barplot(data=df, x="count", y="game_mode", hue="game_mode", palette="magma", legend=False)
    plt.title("Répartition des modes de jeu")
    plt.xlabel("Nombre de batailles")
    plt.ylabel("Mode")
    plt.tight_layout()
    plt.savefig(f"{GRAPH_DIR}/game_modes.png")
    plt.close()

if __name__ == "__main__":
    battles, cards = load_data()
    plot_top_cards(cards)
    plot_results_distribution(battles)
    plot_winrate_by_deck(battles)
    plot_game_modes(battles)
    print("Graphes exportés dans /graphs")