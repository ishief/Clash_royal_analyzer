import json
import os
from dotenv import load_dotenv
from api import get_player_battlelog
from parser import load_battlelog, extract_battles, save_to_csv
from database import (
    create_connection,
    create_tables,
    insert_battle,
    insert_battle_cards
)
load_dotenv()
PLAYER_TAG = os.getenv("PLAYER_TAG")

def save_json(data, filepath):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main():
    battles = get_player_battlelog(PLAYER_TAG)

    if battles is None:
        print("Erreur API sur battlelog.")
        return

    print(f"Nombre de batailles récupérées : {len(battles)}")

    if len(battles) == 0:
        print("Battlelog vide.")
        return

    json_path = "data/raw/player_battles.json"
    csv_path = "data/processed/battles.csv"

    save_json(battles, json_path)
    print(f"Battlelog sauvegardé dans {json_path}")

    battlelog = load_battlelog(json_path)
    rows = extract_battles(battlelog, PLAYER_TAG)
    save_to_csv(rows, csv_path)

    conn = create_connection()
    create_tables(conn)

    for row in rows:
        insert_battle(conn, row)
        insert_battle_cards(conn, row["battle_id"], row["player_deck"], "player")
        insert_battle_cards(conn, row["battle_id"], row["opponent_deck"], "opponent")

    conn.close()
    print("Données insérées dans SQLite : data/royalapi.db")

if __name__ == "__main__":
    main()

