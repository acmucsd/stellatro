# Stellatro

A two-player competitive card game inspired by Balatro, built for bot vs. bot play.

Each player is dealt a hand of cards and drafts jokers (passive modifiers) before playing their best 5-card poker hand. Jokers apply chip and multiplier bonuses during scoring. The player with the higher score wins.

## Project Structure

```
stellatro/
├── src/          # Game logic (game, cards, jokers, hand checker)
├── bots/         # Bot decision logic
│   └── bot.py    # Bot class — implement pick_joker and pick_hand here
├── client/       # Client loop that connects a bot to the game server
│   └── client.py
├── server/       # Flask game server
│   └── server.py
├── Dockerfile.game
├── Dockerfile.bot
├── docker-compose.yml
└── requirements.txt
```

## Running

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
docker compose up --build
```

This starts three containers:
- `stellatro-game` — the game server (port 5000)
- `stellatro-bot1` — Player 1's bot client
- `stellatro-bot2` — Player 2's bot client

Both bots play through a full game and exit. The game server stays up.

## Game Flow

1. **Draft phase** — Players alternate picking jokers from a shared pool. Each player picks 2 jokers total.
2. **Play phase** — Each player submits their best 5-card hand.
3. **Scoring** — Hands are scored using base chip/multiplier values for the hand type, modified by the player's jokers.
4. **Game over** — The player with the higher score wins.

## API

The game server exposes two endpoints.

### `GET /state`

Returns the current game state.

```json
{
  "phase": "DRAFT",
  "current_turn": "PLAYER1",
  "player1_hand": [{ "rank": 10, "suits": ["club"], "scored": true, "num_triggers": 1 }, ...],
  "player2_hand": [...],
  "jokers": [{ "name": "Jolly Joker", "description": "..." }, ...],
  "player1_score": 0,
  "player2_score": 0
}
```

`phase` is one of `DRAFT`, `PLAY`, or `OVER`.
`current_turn` is one of `PLAYER1`, `PLAYER2`, or `null` (when the game is over).

### `POST /step`

Submit a move for the current player.

**Draft phase** — pick a joker by index:
```json
{ "player": 1, "action": 0 }
```

**Play phase** — play 5 cards by index:
```json
{ "player": 1, "hand": [0, 1, 2, 3, 4] }
```

Response:
```json
{ "success": true, "state": { ... } }
```

## Writing a Bot

Edit `bots/bot.py`. The `Bot` class has two methods to implement:

```python
class Bot:
    def pick_joker(self, state) -> int:
        # state is the JSON dict from GET /state
        # return the index of the joker you want to pick
        return 0

    def pick_hand(self, state) -> list[int]:
        # return a list of exactly 5 card indices to play
        # your hand is state["player1_hand"] or state["player2_hand"]
        return [0, 1, 2, 3, 4]
```

The client loop in `client/client.py` handles all server communication. You only need to implement the decision logic in `bot.py`.

## Hand Types (lowest to highest)

| Hand | Base Chips | Base Mult |
|---|---|---|
| High Card | 10 | 1 |
| Pair | 20 | 1 |
| Two Pair | 30 | 2 |
| Three of a Kind | 40 | 2 |
| Straight | 60 | 3 |
| Flush | 70 | 3 |
| Full House | 90 | 4 |
| Four of a Kind | 120 | 5 |
| Straight Flush | 160 | 6 |

Score = (base chips + scored card chips) × multiplier, modified by jokers.
