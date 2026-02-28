import os
import sys
import time
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'bots'))
from bot import Bot

GAME_URL = os.getenv("GAME_URL", "http://game:5000")
PLAYER_ID = int(os.getenv("PLAYER_ID", "1"))


def wait_for_server():
    while True:
        try:
            requests.get(f"{GAME_URL}/state", timeout=2)
            return
        except requests.exceptions.ConnectionError:
            print(f"Bot {PLAYER_ID}: waiting for game server...")
            time.sleep(1)


def main():
    bot = Bot()

    wait_for_server()
    print(f"Bot {PLAYER_ID}: connected to {GAME_URL}")

    while True:
        state = requests.get(f"{GAME_URL}/state").json()
        phase = state["phase"]
        current_turn = state["current_turn"]

        if phase == "OVER":
            print(
                f"Bot {PLAYER_ID}: game over! "
                f"P1: {state['player1_score']} | P2: {state['player2_score']}"
            )
            break

        my_turn = (PLAYER_ID == 1 and current_turn == "PLAYER1") or (
            PLAYER_ID == 2 and current_turn == "PLAYER2"
        )

        if not my_turn:
            time.sleep(0.2)
            continue

        if phase == "DRAFT":
            action = bot.pick_joker(state)
            resp = requests.post(
                f"{GAME_URL}/step",
                json={"player": PLAYER_ID, "action": action},
            ).json()
            print(f"Bot {PLAYER_ID}: picked joker {action} -> success={resp['success']}")

        elif phase == "PLAY":
            hand = bot.pick_hand(state)
            resp = requests.post(
                f"{GAME_URL}/step",
                json={"player": PLAYER_ID, "hand": hand},
            ).json()
            print(f"Bot {PLAYER_ID}: played {hand} -> success={resp['success']}")


if __name__ == "__main__":
    main()
