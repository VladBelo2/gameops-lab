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
  echo "[WARN] ⚠️ Missing $CONFIG_FILE for game '$GAME_NAME' Skipping..."
  exit 0
fi

cd "$GAME_DIR"
APP_NAME=$(jq -r '.app_name' "$CONFIG_FILE")
ENTRY_FILE=$(jq -r '.entry_file' "$CONFIG_FILE")
ASSETS_DIR=$(jq -r '.assets_dir // empty' "$CONFIG_FILE")
WINDOWED=$(jq -r '.windowed' "$CONFIG_FILE")

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
if [[ -f "$VENV_DIR/Scripts/activate" ]]; then
  # Windows
  source "$VENV_DIR/Scripts/activate"
  export PATH="$VENV_DIR/Scripts:$PATH"
elif [[ -f "$VENV_DIR/bin/activate" ]]; then
  # Linux/macOS
  source "$VENV_DIR/bin/activate"
  export PATH="$VENV_DIR/bin:$PATH"
else
  echo "[ERROR] ❌ Failed to find activate script in $VENV_DIR"
  exit 1
fi

# Clean build artifacts
echo "[INFO] 🧹 Cleaning build/, dist/, __pycache__, *.spec..."
rm -rf build dist
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -name '*.spec' -delete

# Install Python packages
echo "[INFO] 🐍 Installing Python packages..."
if [[ "$OS" == "mingw"* || "$OS" == "msys"* || "$OS" == "cygwin"* ]]; then
  PYTHON_CMD="python"
else
  PYTHON_CMD="python3"
fi
"$PYTHON_CMD" -m pip install --upgrade pip
"$PYTHON_CMD" -m pip install pyinstaller pygame

# Build with PyInstaller
echo "[INFO] 🐍 Building with PyInstaller..."
ARGS=(--noconfirm --onedir)
[[ "$WINDOWED" == "true" ]] && ARGS+=(--windowed)
[[ -n "$ASSETS_DIR" ]] && ARGS+=(--add-data "$ASSETS_DIR:$ASSETS_DIR")
ARGS+=(--name "$APP_NAME" "$ENTRY_FILE")

pyinstaller "${ARGS[@]}" 2> >(grep -v "DEPRECATION: Running PyInstaller as root" >&2)

echo "[DONE] ✅ $APP_NAME build complete → dist/$APP_NAME"
