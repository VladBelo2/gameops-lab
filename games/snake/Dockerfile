FROM python:3.10-slim

LABEL maintainer="GameOps Lab" \
      description="Snake game containerized with PyInstaller"

RUN apt-get update && apt-get install -y \
    python3-dev build-essential \
    libgl1 libglib2.0-0 libxrender1 libxext6 \
    xvfb pulseaudio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 👇 Create snake/ in container to match import structure
RUN mkdir snake
COPY . ./snake

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir pygame pyinstaller

RUN pyinstaller --noconfirm --onedir --windowed \
    --add-data "snake/assets:assets" \
    --name snake snake/main.py \
 && chmod +x dist/snake/snake

ENTRYPOINT ["./dist/snake/snake"]
