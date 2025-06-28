#!/usr/bin/env bash
set -e

GAME_NAME="$1"
MODE="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="$SCRIPT_DIR/../games/$GAME_NAME"
DOCKERFILE="$GAME_DIR/Dockerfile"

if [[ -z "$GAME_NAME" ]]; then
  echo "[ERROR] ❌ Game name is required."
  exit 1
fi

if [[ ! -f "$DOCKERFILE" ]]; then
  echo "[ERROR] ❌ No Dockerfile found for $GAME_NAME"
  exit 1
fi

echo "[INFO] 🐳 Building Docker image for $GAME_NAME..."
docker build -t "gameops/$GAME_NAME:latest" -f "$DOCKERFILE" "$GAME_DIR"

if [[ "$MODE" == "--test-only" ]]; then
  echo "[INFO] 🧪 Verifying container in headless mode with xvfb..."
  docker run --rm -e DISPLAY=:99 \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --entrypoint bash \
    "gameops/$GAME_NAME:latest" -c "xvfb-run -a ./dist/$GAME_NAME/main"
else
  echo "[INFO] 🚀 Running container to verify build (HEADLESS_TEST=1)..."
  docker run --rm -e HEADLESS_TEST=1 "gameops/$GAME_NAME:latest"
fi

echo "[SUCCESS] ✅ Docker build + run OK for $GAME_NAME"
