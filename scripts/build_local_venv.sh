#!/usr/bin/env bash
set -e

GAME_NAME="$1"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GAME_DIR="$SCRIPT_DIR/../games/$GAME_NAME"
cd "$GAME_DIR"

CONFIG_FILE="build_config.json"
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "[ERROR] ❌ Missing $CONFIG_FILE in $GAME_DIR"
  exit 1
fi

GLOBAL_VENV="$2"
APP_NAME=$(jq -r '.app_name' "$CONFIG_FILE")
ENTRY_FILE=$(jq -r '.entry_file' "$CONFIG_FILE")
ASSETS_DIR=$(jq -r '.assets_dir // empty' "$CONFIG_FILE")
VENV_DIR=${GLOBAL_VENV:-$(jq -r '.venv_dir' "$CONFIG_FILE")}
WINDOWED=$(jq -r '.windowed' "$CONFIG_FILE")

echo "[INFO] 🛠️ Building $APP_NAME..."

# Clean .venv to avoid interpreter mismatch across platforms
echo "[INFO] 🧹 Removing old virtual environment: $VENV_DIR"
[[ -d "$VENV_DIR" ]] && rm -rf "$VENV_DIR" || true
sleep 3
# if [[ -d "$VENV_DIR" ]]; then
#   echo "[INFO] 🧹 Removing old virtual environment: $VENV_DIR"
#   chmod -R u+rw "$VENV_DIR" 2>/dev/null || true
#   rm -rf "$VENV_DIR" 2>/dev/null || true

#   if [[ -d "$VENV_DIR" ]]; then
#     echo "[WARN] ⚠️ Standard rm -rf failed. Using fallback cleanup..."
#     find "$VENV_DIR" -type f -exec rm -f {} \; 2>/dev/null || true
#     find "$VENV_DIR" -type d -exec chmod u+rwx {} \; 2>/dev/null || true
#     find "$VENV_DIR" -depth -type d -exec rmdir {} \; 2>/dev/null || true
#     rmdir "$VENV_DIR" 2>/dev/null || true
#   fi

#   if [[ -d "$VENV_DIR" ]]; then
#     echo "[FATAL] ❌ Could not delete $VENV_DIR. Please close any open terminals or editors using it."
#     exit 1
#   fi
# fi

# Create new venv
echo "[INFO] 🧪 Creating new virtual environment at $VENV_DIR..."
/usr/bin/python3 -m venv "$VENV_DIR"

# Activate venv
if [[ -f "$VENV_DIR/bin/activate" ]]; then
  source "$VENV_DIR/bin/activate"
  export PATH="$VENV_DIR/bin:$PATH"
else
  echo "[ERROR] ❌ Failed to activate virtualenv in $VENV_DIR"
  exit 1
fi

# Clean old build artifacts
echo "[INFO] 🧹 Cleaning build/, dist/, __pycache__, *.spec..."

# Clean build/
[[ -d build ]] && rm -rf build || true

# Clean dist/
[[ -d dist ]] && rm -rf dist || true

# Clean __pycache__ recursively
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true

# Delete .spec files
find . -name '*.spec' -delete

echo "[INFO] 🐍 Install Python & Dependencies"
# Install build dependencies
pip install --upgrade pip
pip install pyinstaller pygame

echo "[INFO] 🐍 Build with PyInstaller"
# Build with PyInstaller
ARGS=(--noconfirm --onedir)
[[ "$WINDOWED" == "true" ]] && ARGS+=(--windowed)
[[ -n "$ASSETS_DIR" ]] && ARGS+=(--add-data "$ASSETS_DIR:$ASSETS_DIR")
# [[ -n "$ASSETS_DIR" ]] && ARGS+=(--add-data "$GAME_NAME/$ASSETS_DIR:$ASSETS_DIR")
ARGS+=(--name "$APP_NAME" "$ENTRY_FILE")

pyinstaller "${ARGS[@]}" 2> >(grep -v "DEPRECATION: Running PyInstaller as root" >&2)

echo "[DONE] ✅ $APP_NAME build complete → dist/$APP_NAME"
