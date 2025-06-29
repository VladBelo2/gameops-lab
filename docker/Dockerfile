# docker/Dockerfile

FROM python:3.10-slim

LABEL maintainer="GameOps Lab" \
      description="Containerized build for GameOps Lab games"

# System dependencies for Pygame + PyInstaller
RUN apt-get update && apt-get install -y \
    python3-dev build-essential \
    libgl1 libglib2.0-0 libxrender1 libxext6 \
    xvfb pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Set working dir and environment
WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Accept build arg
ARG GAME_NAME
ENV GAME_NAME=$GAME_NAME

# Create game directory and copy all project files
COPY $GAME_NAME /app/$GAME_NAME

# Install dependencies
RUN pip install --no-cache-dir pygame pyinstaller

# Build the game binary
RUN pyinstaller --noconfirm --onedir --windowed \
    # --add-data "$GAME_NAME/assets:$GAME_NAME/_internal/assets" \
    --add-data "$GAME_NAME/assets:assets" \
    --name $GAME_NAME $GAME_NAME/main.py \
 && chmod +x dist/$GAME_NAME/$GAME_NAME

ENTRYPOINT ["sh", "-c", "./dist/$GAME_NAME/$GAME_NAME"]
