# Docker Setup

## Overview

The evaluation runs across three containers on a shared private network:

```
┌─────────────────────────────────────────┐
│           stellatro-net (bridge)         │
│                                         │
│  ┌─────────────┐     ┌───────────────┐  │
│  │ stellatro-  │     │ stellatro-    │  │
│  │ bot1        │────▶│ game          │  │
│  │ (PLAYER_ID=1│     │ :5000         │  │
│  └─────────────┘     └───────────────┘  │
│                              ▲          │
│  ┌─────────────┐             │          │
│  │ stellatro-  │─────────────┘          │
│  │ bot2        │                        │
│  │ (PLAYER_ID=2│                        │
│  └─────────────┘                        │
└─────────────────────────────────────────┘
         (also exposed on host :5000)
```

- **stellatro-game** runs the Flask game server. It holds all game state and exposes the API.
- **stellatro-bot1** and **stellatro-bot2** each run a copy of the bot client, differentiated by the `PLAYER_ID` environment variable. They connect to the game server, poll for their turn, and submit moves until the game ends.

## Dockerfiles

### `Dockerfile.game`

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY server/ ./server/

ENV PYTHONPATH=/app/src

CMD ["python", "server/server.py"]
```

- Installs `flask` and `requests` from `requirements.txt`.
- Copies `src/` (game logic) and `server/` (Flask app) separately so that `server.py` stays outside the game logic directory.
- Sets `PYTHONPATH=/app/src` so that `server.py` can import from `src/` (e.g. `from game import Game`) without any path manipulation in the source code.
- Runs `server/server.py` as the main process. The container stays alive as long as the Flask server is running.

### `Dockerfile.bot`

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY bots/ ./bots/
COPY client/ ./client/

CMD ["python", "client/client.py"]
```

- Uses the same base image and `requirements.txt` as the game container (both images share cached layers, so the pip install only runs once).
- Copies `src/` in case bot logic eventually needs game types, `bots/` for the `Bot` class, and `client/` for the client loop.
- `client.py` imports `Bot` from `bots/bot.py` using a relative `sys.path` insertion.
- The container exits when the game ends (i.e. when `client.py` reaches the `OVER` phase and breaks out of the loop).

## docker-compose.yml

### Services

**game**
```yaml
game:
  build:
    context: .
    dockerfile: Dockerfile.game
  container_name: stellatro-game
  ports:
    - "5000:5000"
  networks:
    - stellatro-net
```
The `context: .` means the entire project root is sent to the Docker build daemon, which is necessary since the Dockerfile references multiple top-level directories. Port 5000 is published to the host so you can hit the API directly with `curl` or a browser during development.

**bot1 / bot2**
```yaml
bot1:
  build:
    context: .
    dockerfile: Dockerfile.bot
  container_name: stellatro-bot1
  environment:
    - PLAYER_ID=1
  depends_on:
    - game
  networks:
    - stellatro-net
```
Both bot services are built from the same `Dockerfile.bot` — the only difference is `PLAYER_ID`. `depends_on: game` ensures Docker starts the game container first, though it does not wait for Flask to be ready. The client handles this with a retry loop (`wait_for_server` in `client.py`).

### Networking

```yaml
networks:
  stellatro-net:
    driver: bridge
```

All three containers are attached to a user-defined bridge network called `stellatro-net`. On this network, each container is reachable by its **service name** as a hostname. The bot clients connect to `http://game:5000` — Docker's internal DNS resolves `game` to the game container's IP automatically.

## Running an Evaluation

### Full run (foreground)

```bash
docker compose up --build
```

Builds all images (or uses cache if nothing changed), starts all three containers, and streams logs from all of them. Press `Ctrl+C` to stop everything.

### Full run (detached)

```bash
docker compose up --build -d
```

Runs in the background. Use the commands below to observe what's happening.

### Useful commands

```bash
# Stream logs from all containers
docker compose logs -f

# Stream logs from one container
docker compose logs -f game
docker compose logs -f bot1

# Check container status
docker compose ps

# Stop and remove containers (keeps images)
docker compose down

# Rebuild a single image without cache
docker compose build --no-cache game

# Open a shell inside a running container
docker exec -it stellatro-game bash

# Hit the game API directly from the host
curl http://localhost:5000/state
```

### Rebuilding after code changes

Docker caches each build step. If you only change Python files (not `requirements.txt`), the pip install step is skipped and rebuilds are fast:

```bash
docker compose up --build
```

If you add a new dependency to `requirements.txt`, the cache for the pip install layer is invalidated and all subsequent layers are rebuilt for both images.
