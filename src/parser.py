import json
import csv

def load_battlelog(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_battles(battlelog: list[dict], player_tag: str):
    rows = []

    for i, battle in enumerate(battlelog):
        battle_time = battle.get("battleTime")
        game_mode = battle.get("gameMode", {}).get("name")

        team = battle.get("team", [])
        opponent = battle.get("opponent", [])

        if not team or not opponent:
            continue

        player = team[0]
        enemy = opponent[0]

        crowns_player = player.get("crowns")
        crowns_opponent = enemy.get("crowns")

        if crowns_player > crowns_opponent:
            result = "win"
        elif crowns_player < crowns_opponent:
            result = "loss"
        else:
            result = "draw"

        player_cards = [card.get("name") for card in player.get("cards", [])]
        opponent_cards = [card.get("name") for card in enemy.get("cards", [])]

        row = {
            "battle_id": f"{player_tag}_{i}",
            "battle_time": battle_time,
            "player_tag": "PLAYER_TEST",
            "opponent_tag": "OPPONENT_HIDDEN",
            "game_mode": game_mode,
            "crowns_player": crowns_player,
            "crowns_opponent": crowns_opponent,
            "result": result,
            "player_deck": " | ".join(player_cards),
            "opponent_deck": " | ".join(opponent_cards)
        }

        rows.append(row)

    return rows

def save_to_csv(rows, filepath):
    if not rows:
        print("Aucune ligne à sauvegarder.")
        return

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV sauvegardé : {filepath}")