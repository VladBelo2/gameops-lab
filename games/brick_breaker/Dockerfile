FROM python:3.10-slim

LABEL maintainer="GameOps Lab" \
      description="Brick Breaker game containerized with PyInstaller"

RUN apt-get update && apt-get install -y \
    python3-dev build-essential \
    libgl1 libglib2.0-0 libxrender1 libxext6 \
    xvfb pulseaudio \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 👇 Create brick_breaker/ in container to match import structure
RUN mkdir brick_breaker
COPY . ./brick_breaker

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir pygame pyinstaller

RUN pyinstaller --noconfirm --onedir --windowed \
    --add-data "brick_breaker/assets:assets" \
    --name brick_breaker brick_breaker/main.py \
 && chmod +x dist/brick_breaker/brick_breaker

ENTRYPOINT ["./dist/brick_breaker/brick_breaker"]
