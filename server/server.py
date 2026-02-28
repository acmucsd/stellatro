from flask import Flask, jsonify, request
from game import Game, Phase, PlayerTurn

app = Flask(__name__)

game = Game()
game.start_round()


def serialize_card(card):
    return {
        "rank": card.rank,
        "suits": sorted([s.value for s in card.suits]),
        "scored": card.scored,
        "num_triggers": card.num_triggers,
    }


def serialize_joker(joker):
    return {
        "name": joker.name,
        "description": joker.description,
    }


def serialize_state(state):
    return {
        "phase": state.phase.name,
        "current_turn": state.current_turn.name if state.current_turn else None,
        "player1_hand": [serialize_card(c) for c in state.player1_hand],
        "player2_hand": [serialize_card(c) for c in state.player2_hand],
        "jokers": [serialize_joker(j) for j in state.jokers],
        "player1_score": state.player1_score,
        "player2_score": state.player2_score,
    }


@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(serialize_state(game.get_game_state()))


@app.route("/step", methods=["POST"])
def step():
    data = request.get_json()
    if data is None:
        return jsonify({"success": False, "error": "No JSON body"}), 400

    player = data.get("player")
    if player not in (1, 2):
        return jsonify({"success": False, "error": "Invalid player"}), 400

    action = data.get("action")   # used in DRAFT phase
    hand = data.get("hand")       # used in PLAY phase

    success, state = game.step(player, action=action, hand_list=hand)
    return jsonify({"success": success, "state": serialize_state(state)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
