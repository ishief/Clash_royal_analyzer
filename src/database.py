import sqlite3

def create_connection(db_path: str ="data/royalapi.db"):
    return sqlite3.connect(db_path)

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS battles (
        battle_id TEXT PRIMARY KEY,
        battle_time TEXT,
        player_tag TEXT,
        opponent_tag TEXT,
        game_mode TEXT,
        result TEXT,
        crowns_player INTEGER,
        crowns_opponent INTEGER,
        player_deck TEXT,
        opponent_deck TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS battle_cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        battle_id TEXT,
        card_name TEXT,
        owner TEXT,
        FOREIGN KEY (battle_id) REFERENCES battles (battle_id)
    )
    """)

    conn.commit()

def insert_battle(conn, row):
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO battles (
        battle_id, battle_time, player_tag, opponent_tag,
        game_mode, result, crowns_player, crowns_opponent,
        player_deck, opponent_deck
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row["battle_id"],
        row["battle_time"],
        row["player_tag"],
        row["opponent_tag"],
        row["game_mode"],
        row["result"],
        row["crowns_player"],
        row["crowns_opponent"],
        row["player_deck"],
        row["opponent_deck"]
    ))

    conn.commit()

def insert_battle_cards(conn, battle_id, deck_string, owner):
    cursor = conn.cursor()
    cards = deck_string.split(" | ")

    for card in cards:
        cursor.execute("""
        INSERT INTO battle_cards (battle_id, card_name, owner)
        VALUES (?, ?, ?)
        """, (battle_id, card, owner))

    conn.commit()