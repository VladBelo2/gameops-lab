#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/.."
cd "$ROOT_DIR"

GAME_NAME="$1"

# Handle 'all' or empty input → build all games
if [[ -z "$GAME_NAME" || "$GAME_NAME" == "all" ]]; then
  echo "[INFO] 🚀 Building all games..."
  GAMES=($(jq -r '.games[]' games.json))
  for GAME in "${GAMES[@]}"; do
    echo "────────────────────────────────────────"
    echo "[INFO] 🎮 Building $GAME..."
    bash "$SCRIPT_DIR/build_local_venv.sh" "$GAME" || echo "[WARN] ⚠️ Skipped $GAME due to errors"
  done
  echo "────────────────────────────────────────"
  echo "[SUCCESS] ✅ All builds attempted."
  exit 0
fi

# Single game logic
GAME_DIR="$ROOT_DIR/games/$GAME_NAME"
CONFIG_FILE="$GAME_DIR/build_config.json"

if [[ ! -d "$GAME_DIR" ]]; then
  echo "[WARN] ⚠️ Game folder '$GAME_NAME' does not exist. Skipping..."
  exit 0
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "[WARN] ⚠️ Missing $CONFIG_FILE for game '$GAME_NAME'. Skipping..."
  exit 0
fi

cd "$GAME_DIR"
APP_NAME=$(jq -r '.app_name' "$CONFIG_FILE")
ASSETS_DIR=$(jq -r '.assets_dir // empty' "$CONFIG_FILE")

echo "[INFO] 🛠️ Building $APP_NAME..."

# OS-specific venv logic
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
if [[ "$OS" == "linux" && "$USER" == "vagrant" ]]; then
  VENV_DIR="/home/vagrant/venvs/${GAME_NAME}/.venv-${OS}"
else
  VENV_DIR="$GAME_DIR/.venv-${OS}"
fi

echo "[INFO] 🧪 Using virtual environment at: $VENV_DIR"
mkdir -p "$(dirname "$VENV_DIR")"
if [[ ! -d "$VENV_DIR" ]]; then
  echo "[INFO] 🧪 Creating virtualenv: $VENV_DIR"
  python3 -m venv "$VENV_DIR"
fi

# Activate venv
if [[ -f "$VENV_DIR/bin/activate" ]]; then
  if [[ "$OS" == mingw* || "$OS" == msys* || "$OS" == cygwin* ]]; then
    source "$VENV_DIR/Scripts/activate"
  else
    source "$VENV_DIR/bin/activate"
  fi
  export PATH="$VENV_DIR/bin:$PATH"
else
  echo "[ERROR] ❌ Failed to activate virtualenv in $VENV_DIR"
  exit 1
fi

# Clean build artifacts
echo "[INFO] 🧹 Cleaning build/, dist/, __pycache__, *.spec..."
rm -rf build dist
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.spec' -delete

# Install Python dependencies
echo "[INFO] 🐍 Installing Python packages..."
pip install --upgrade pip
pip install pygame

echo "[DONE] ✅ $APP_NAME build complete → dist/$APP_NAME"
