#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

source /vagrant/env.conf
BUILD_FAILED=false

header() {
  echo "────────────────────────────────────────"
  echo "$1"
  echo "────────────────────────────────────────"
}

header "[STEP] 📦 System & Python Setup"

echo "[INFO] 🐍 Installing Python $PYTHON_VERSION and pip..."
apt-get update -y
apt-get upgrade -y
apt-get install -y \
  "python${PYTHON_VERSION}" \
  "python${PYTHON_VERSION}-venv" \
  "python${PYTHON_VERSION}-dev" \
  python3-pip build-essential jq

header "[STEP] 🧪 Creating Python Virtual Environment"

GAME_NAME="devops-lab"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
VENV_DIR="/root/venvs/${GAME_NAME}/.venv-${OS}"

mkdir -p "$(dirname "$VENV_DIR")"
if [[ ! -d "$VENV_DIR" ]]; then
  python${PYTHON_VERSION} -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PATH="$VENV_DIR/bin:$PATH"

echo "[INFO] 🔄 Auto-activating venv on login..."
grep -q "$VENV_DIR/bin/activate" /root/.bashrc || echo "source $VENV_DIR/bin/activate" >> /root/.bashrc

echo "[INFO] 🐍 Installing Python packages in venv..."
pip install --upgrade pip
[[ "$INSTALL_PYTEST" == "true" ]] && pip install pytest

header "[STEP] 🛠️ Building and Testing Games"

GAMES=($(jq -r '.games[]' /vagrant/games.json))
for GAME in "${GAMES[@]}"; do
  echo ""
  echo "🎮 [$GAME] 🔧 Building with virtualenv..."
  bash /vagrant/scripts/build_local_venv.sh "$GAME" "/vagrant/.venv" \
    && echo "✅ Build succeeded for $GAME" \
    || { echo "❌ Build failed for $GAME"; BUILD_FAILED=true; }

  if [[ "$INSTALL_PYTEST" == "true" ]]; then
    echo "🧪 [$GAME] Running Tests..."
    pytest "/vagrant/games/$GAME/tests" \
      && echo "✅ Tests passed for $GAME" \
      || { echo "❌ Tests failed for $GAME"; BUILD_FAILED=true; }
  fi

  echo "🐳 [$GAME] Docker Build and Headless Test..."
  bash /vagrant/docker/build_docker_image.sh "$GAME" --test-only \
    && echo "✅ Docker build passed for $GAME" \
    || { echo "❌ Docker build failed for $GAME"; BUILD_FAILED=true; }
done

echo ""
if [[ "$BUILD_FAILED" == "true" ]]; then
  echo "[DONE] ⚠️ Provisioning completed with some errors."
else
  echo "[DONE] ✅ Provisioning completed successfully!"
fi
