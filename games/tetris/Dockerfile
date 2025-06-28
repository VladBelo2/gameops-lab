FROM python:3.10-slim

LABEL maintainer="GameOps Lab" \
      description="Tetris game containerized with PyInstaller"

RUN apt-get update && apt-get install -y \
    python3-dev build-essential \
    libgl1 libglib2.0-0 libxrender1 libxext6 \
    xvfb pulseaudio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 👇 Create tetris/ in container to match import structure
RUN mkdir tetris
COPY . ./tetris

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir pygame pyinstaller

RUN pyinstaller --noconfirm --onedir --windowed \
    --add-data "tetris/assets:assets" \
    --name tetris tetris/main.py \
 && chmod +x dist/tetris/tetris

ENTRYPOINT ["./dist/tetris/tetris"]
