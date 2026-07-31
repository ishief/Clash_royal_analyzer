import sqlite3
import pandas as pd

DB_PATH = "data/royalapi.db"

def load_data():
    conn = sqlite3.connect(DB_PATH)

    battles = pd.read_sql_query("SELECT * FROM battles", conn)
    cards = pd.read_sql_query("SELECT * FROM battle_cards", conn)

    conn.close()
    return battles, cards

def global_stats(battles):
    total = len(battles)
    wins = len(battles[battles["result"] == "win"])
    losses = len(battles[battles["result"] == "loss"])
    draws = len(battles[battles["result"] == "draw"])
    winrate = round((wins / total) * 100, 2) if total > 0 else 0

    stats = {
        "total_battles": total,
        "wins": wins,
        "losses": losses,
        "draws": draws,
        "winrate_global": winrate,
        "avg_crowns_player": round(battles["crowns_player"].mean(), 2),
        "avg_crowns_opponent": round(battles["crowns_opponent"].mean(), 2),
    }

    return stats

def top_cards(cards, top_n=10):
    return (
        cards[cards["owner"] == "player"]["card_name"]
        .value_counts()
        .head(top_n)
        .reset_index()
        .rename(columns={"index": "card_name", "card_name": "count"})
    )

def winrate_by_deck(battles, min_matches=2):
    grouped = battles.groupby("player_deck").agg(
        matches=("battle_id", "count"),
        wins=("result", lambda x: (x == "win").sum())
    ).reset_index()

    grouped["winrate"] = round((grouped["wins"] / grouped["matches"]) * 100, 2)
    grouped = grouped[grouped["matches"] >= min_matches]
    grouped = grouped.sort_values(by="winrate", ascending=False)

    return grouped

def game_mode_stats(battles):
    return battles["game_mode"].value_counts().reset_index().rename(
        columns={"index": "game_mode", "game_mode": "count"}
    )

if __name__ == "__main__":
    battles, cards = load_data()

    print("=== STATS GLOBALES ===")
    print(global_stats(battles))

    print("\n=== TOP CARTES ===")
    print(top_cards(cards))

    print("\n=== WINRATE PAR DECK ===")
    print(winrate_by_deck(battles))

    print("\n=== MODES DE JEU ===")
    print(game_mode_stats(battles))