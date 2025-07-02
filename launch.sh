#!/bin/bash
set -e

echo "[INFO] 🚀 Starting Docker build and provisioning..."
docker-compose down -v

echo "[INFO] 🔨 Building container..."
docker-compose build

echo "[INFO] 🔄 Running container in background (detached)..."
docker-compose up -d

echo "[INFO] 🧪 Running provisioning script inside the container..."
docker exec gameops-container bash /vagrant/provision_docker.sh

echo "[INFO] ✅ All done!"
echo "[INFO] 📡 To view logs: docker logs -f gameops-container"
echo "[INFO] 🐚 To enter shell: docker exec -it gameops-container bash"
