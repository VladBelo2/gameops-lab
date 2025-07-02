#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

GAME_NAME="$1"
MODE="$2"

# Interpret test options
SKIP_TEST=false
if [[ "$MODE" == "--no-test" ]]; then
  SKIP_TEST=true
elif [[ "$MODE" == "--test-only" ]]; then
  SKIP_TEST=false
fi

# Handle all or missing game
if [[ -z "$GAME_NAME" || "$GAME_NAME" == "all" ]]; then
  echo "[INFO] 🐳 Building Docker images for all games..."
  GAMES=($(jq -r '.games[]' games.json))
  for GAME in "${GAMES[@]}"; do
    echo "────────────────────────────────────────"
    echo "[INFO] 🧱 Building $GAME..."
    bash "$SCRIPT_DIR/build_docker_image.sh" "$GAME" "$MODE" || echo "[WARN] ⚠️ Skipped $GAME due to errors"
  done
  echo "────────────────────────────────────────"
  echo "[SUCCESS] ✅ All Docker builds attempted."
  exit 0
fi

# Single game build
GAME_DIR="$ROOT_DIR/games/$GAME_NAME"
DOCKERFILE="$GAME_DIR/Dockerfile"

if [[ ! -d "$GAME_DIR" ]]; then
  echo "[WARN] ⚠️ Game folder '$GAME_NAME' not found. Skipping..."
  exit 0
fi

if [[ ! -f "$DOCKERFILE" ]]; then
  echo "[WARN] ⚠️ No Dockerfile for $GAME_NAME. Skipping..."
  exit 0
fi

if [[ ! -f "$GAME_DIR/main.py" ]]; then
  echo "[WARN] ⚠️ Missing main.py for $GAME_NAME. Skipping..."
  exit 0
fi

if [[ ! -d "$GAME_DIR/assets" ]]; then
  echo "[WARN] ⚠️ Missing assets/ folder for $GAME_NAME. Skipping..."
  exit 0
fi

echo "[INFO] 🐳 Building Docker image for $GAME_NAME..."
docker build -t "gameops/$GAME_NAME:latest" -f "$DOCKERFILE" "$GAME_DIR"

if [[ "$SKIP_TEST" == true ]]; then
  echo "[INFO] ⏭️ Skipping post-build test (--no-test)"
elif [[ "$MODE" == "--test-only" ]]; then
  echo "[INFO] 🧪 Verifying container in headless mode (no xvfb)..."
  docker run --rm -e HEADLESS_TEST=1 "gameops/$GAME_NAME:latest"
else
  echo "[INFO] 🚀 Running container to verify build (HEADLESS_TEST=1)..."
  docker run --rm -e HEADLESS_TEST=1 "gameops/$GAME_NAME:latest"
fi

echo "[SUCCESS] ✅ Docker build + run OK for $GAME_NAME"
