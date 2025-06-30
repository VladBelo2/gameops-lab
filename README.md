# 🕹️ GameOps Lab 🎲

**GameOps Lab** is a cross-platform DevOps game automation lab. It features 3 classic arcade-style games — Tetris, Brick Breaker, and Snake — that are built, tested, and packaged automatically for macOS, Windows, and Linux using GitHub Actions CI/CD.

Each game is written in Python with `pygame`, built with `pyinstaller` or `py2app`, and Dockerized for headless verification. The project emphasizes DevOps best practices, cross-platform delivery, and reproducible builds in a fully automated environment.

---

## 📦 Features

- 🎮 Three classic games: **Tetris**, **Brick Breaker**, and **Snake**
- 🐳 Docker builds and headless tests for every game
- 🧪 Full GitHub Actions matrix CI for macOS, Windows, and Linux
- 🖼️ PyInstaller and py2app builds for native .exe / .app / .AppImage outputs
- ✅ Per-game `build_config.json` and automated builders
- 💻 Vagrant VM with auto-provisioning via `provision.sh`
- 🧠 Game-specific testing and linting (with `pytest`)
- 🗃️ Dynamic build matrix powered by `games.json`

---

## 📁 Project Structure

games/
├── tetris/
├── brick_breaker/
└── snake/
docker/
├── build_docker_image.sh
├── Makefile
.github/
├── workflows/
└── actions/
scripts/
├── build_local_venv.sh
└── build_all.sh

---

## 🚀 Usage

### 🧪 Run Everything (inside Vagrant)

```bash
vagrant destroy -f && vagrant up
```

🧱 Manual Game Build (inside VM)

```bash
bash scripts/build_local_venv.sh tetris
bash docker/build_docker_image.sh tetris
```

🧱 Manual Game Build (on Host)

```bash
bash build_all.sh
```

Host builds only support macOS/Linux. Use the VM for reproducible builds.

---

## ⚙️ Configuration

- env.conf — toggles (install Docker, PyInstaller, etc.)

- games.json — list of games to build

- build_config.json (per game) — build name, entry file, assets, flags

---

## 🏗️ CI/CD Pipeline

GitHub Actions auto-builds all games per platform:

- .github/actions/build-game/ — reusable build logic per OS

- docker.yml — dynamic matrix using games.json

- Uploads .exe, .app, .AppImage as artifacts

---

## 🔐 Signing & Notarization

Currently skipped. May be added later for .dmg and .exe builds using:

- macOS: codesign, Apple Dev account

- Windows: signtool, valid certificate

---

## 💡 Contributions

Want to add your own game? Just:

- Add a folder under games/your_game

- Create a build_config.json

- Add the game name to games.json

---

## 🔮 Coming Next: Future Phases

The GameOps Lab project is actively evolving! Here are the upcoming development phases planned:

Phase	Title	Description
✅ Phase 1	🎮 Game Dev Foundation	Build 3 fully playable Python games using Pygame.
✅ Phase 2	🐳 Docker Builds	Containerize each game and test headless builds.
✅ Phase 3	🔁 GitHub Actions Matrix	Cross-platform builds for all games via CI/CD.
✅ Phase 4	📦 Native Installers	Generate .exe, .app, and .AppImage binaries.
🔜 Phase 5	☸️ Kubernetes Deployment	Deploy all games in a headless K8s lab with Ingress.
🔜 Phase 6	📊 Monitoring with Prometheus & Grafana	Add observability: game pod crashes, restarts, metrics.
🔜 Phase 7	🤖 Game Bots	Simulate gameplay using bots for load testing.
🔜 Phase 8	💥 Chaos Engineering	Simulate random crashes and ensure system resilience.
🔜 Phase 9	🚀 GitOps with ArgoCD	Declarative GitOps-based game deployment pipeline.
🔜 Phase 10	🌐 Public Download Portal	Host binaries and allow users to download games directly.

---

## 📄 License

MIT License. See LICENSE.

---

## 👨‍🔧 Authors

Developed by Vlad Belo as part of the GameOps Lab portfolio project.
