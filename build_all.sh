#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[INFO] 🚀 Building all games..."

# GAMES=("snake")
GAMES=("brick_breaker" "snake" "tetris")

for GAME in "${GAMES[@]}"; do
  echo "[INFO] 🎮 Building $GAME..."
  bash scripts/build_local_venv.sh "$GAME"
done

echo "[SUCCESS] ✅ All builds complete."
