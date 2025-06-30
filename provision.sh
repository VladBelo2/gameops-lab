#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

source /vagrant/env.conf
BUILD_FAILED=false

echo "────────────────────────────────────────"
echo "[STEP] 📦 System & Python Setup"
echo "────────────────────────────────────────"

echo "[INFO] 🐍 Installing Python $PYTHON_VERSION and pip..."
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv" \
  "python${PYTHON_VERSION}-dev" python3-pip build-essential jq

if [[ "$INSTALL_PYGAME_DEPS" == "true" ]]; then
  echo "[INFO] 🎮 Installing SDL2 and GUI dependencies..."
  sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libfreetype6-dev libavformat-dev libswscale-dev \
    libjpeg-dev libpng-dev libtiff-dev libx11-dev
fi

echo "────────────────────────────────────────"
echo "[STEP] 🐳 Installing Docker Engine"
echo "────────────────────────────────────────"

# Install prerequisites
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker’s official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repo
echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update again and install Docker
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add vagrant user to docker group
sudo usermod -aG docker vagrant

# Verify
if docker --version >/dev/null 2>&1; then
  echo "✅ Docker installed: $(docker --version)"
else
  echo "❌ Docker installation failed!"
  exit 1
fi

echo "────────────────────────────────────────"
echo "[STEP] 🧪 Creating Python Virtual Environment"
echo "────────────────────────────────────────"

echo "[INFO] 🧪 Creating Python virtual environment with OS isolation..."
GAME_NAME="devops-lab"  # or generic label
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
VENV_DIR="/home/vagrant/venvs/${GAME_NAME}/.venv-${OS}"

mkdir -p "$(dirname "$VENV_DIR")"
if [[ ! -d "$VENV_DIR" ]]; then
  python${PYTHON_VERSION} -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
export PATH="$VENV_DIR/bin:$PATH"

echo "[INFO] 🔄 Auto-activating venv on login..."
grep -q "$VENV_DIR/bin/activate" /home/vagrant/.bashrc || echo "source $VENV_DIR/bin/activate" >> /home/vagrant/.bashrc

echo "[INFO] 🐍 Installing Python packages in venv..."
pip install --upgrade pip
[[ "$INSTALL_PYGAME_DEPS" == "true" ]] && pip install pygame
[[ "$INSTALL_PYINSTALLER" == "true" ]] && pip install pyinstaller
[[ "$INSTALL_PYTEST" == "true" ]] && pip install pytest

echo "────────────────────────────────────────"
echo "[STEP] 🛠️ Building and Testing Games"
echo "────────────────────────────────────────"

# GAMES=("tetris" "brick_breaker" "snake")
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
    # for i in {1..10}; do pytest "/vagrant/games/$GAME/tests" || break; done
  fi

  echo "🐳 [$GAME] Docker Build and Headless Test..."
  bash /vagrant/docker/build_docker_image.sh "$GAME" \
    && echo "✅ Docker build passed for $GAME" \
    || { echo "❌ Docker build failed for $GAME"; BUILD_FAILED=true; }
done

echo ""
if [[ "$BUILD_FAILED" == "true" ]]; then
  echo "[DONE] ⚠️ Provisioning completed with some errors."
else
  echo "[DONE] ✅ Provisioning completed successfully!"
fi

echo "[INFO] ℹ️ Docker group changes require logout. Run: exec su - vagrant"
