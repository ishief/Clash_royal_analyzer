from dotenv import load_dotenv
import os
import requests

load_dotenv()

API_KEY = os.getenv("PROJET_ROYALAPI")

if not API_KEY:
    raise ValueError("PROJET_ROYALAPI introuvable dans le fichier .env")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

def format_tag(player_tag: str) -> str:
    return player_tag.replace("#", "%23").strip()

def get_player(player_tag: str):
    tag = format_tag(player_tag)
    url = f"https://api.clashroyale.com/v1/players/{tag}"
    response = requests.get(url, headers=HEADERS)

    print(f"GET {url} -> {response.status_code}")

    if response.status_code == 200:
        return response.json()

    print("Erreur API :", response.text)
    return None

def get_player_battlelog(player_tag: str):
    tag = format_tag(player_tag)
    url = f"https://api.clashroyale.com/v1/players/{tag}/battlelog"
    response = requests.get(url, headers=HEADERS)

    print(f"GET {url} -> {response.status_code}")

    if response.status_code == 200:
        return response.json()

    print("Erreur API :", response.text)
    return None