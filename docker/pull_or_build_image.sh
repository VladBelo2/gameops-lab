#!/usr/bin/env bash
set -e

GAME="$1"
IMAGE="vladbelo2/$GAME:latest"

if [[ "${USE_DOCKERHUB_IMAGES:-false}" == "true" ]]; then
  echo "[INFO] 🐳 Pulling $IMAGE from Docker Hub..."
  docker pull "$IMAGE"
else
  echo "[INFO] 🔨 Building $GAME locally from Dockerfile..."
  bash /vagrant/docker/build_docker_image.sh "$GAME"
fi
