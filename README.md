# 🕹️ GameOps Lab 🎲

**GameOps Lab** is a cross-platform DevOps automation project that turns classic arcade-style games into a real-world CI/CD and infrastructure playground. It includes **Tetris**, **Brick Breaker**, and **Snake**, built using Python and pygame, and packaged for **macOS**, **Windows**, and **Linux**.

This project automates everything: building, testing, containerizing, and packaging — using GitHub Actions, Vagrant, and Docker. It’s designed to demonstrate real-world DevOps practices across platforms in a reproducible, automated, and scalable way.

---

## 📦 Features

- 🎮 Three classic games: Tetris, Brick Breaker, Snake
- 🧪 Headless Docker builds and PyInstaller packaging
- 🐧 GitHub Actions CI/CD matrix for Linux, macOS (Intel+ARM), and Windows
- 📦 Native `.exe`, `.app`, and `.AppImage` outputs
- 💻 Fully automated Vagrant + provision.sh build system
- 📁 Per-game `build_config.json` and global `games.json` for centralized control
- ✅ Tests via `pytest` and cross-platform `.venv` handling
- 🐍 Custom Docker and VM build runners with CLI tooling
- 📜 Build logs, artifacts, and game packages as GitHub Action outputs

---

## 📁 Project Structure

```text
games/
├── tetris/
├── brick_breaker/
└── snake/
docker/
├── build_docker_image.sh
├── Makefile
.github/
└── workflows/
scripts/
└── build_local_venv.sh
```

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

- `env.conf` — toggles for VM provisioning (Docker, PyInstaller, etc.)
- `games.json` — list of game names used for build matrix
- `build_config.json` (per game) — controls:

  - `app_name`

  - `entry_file`

  - `assets_dir`

  - `venv_dir`

  - `windowed` build

---

## 🏗️ CI/CD Pipeline (GitHub Actions)

- 💡 Automatically builds every game for every OS
- ✅ Dynamic matrix from games.json
- 📁 Uploads .exe, .app, .AppImage as build artifacts
- 🔧 Full VM + Docker provisioning workflows:

  - `spin_vm.yml` — Provisions and copies project from GitHub

  - `spin_docker.yml` — Builds dynamic container with pip/pkg options

---

## 🐳 DevOps-Orchestrator Integration

This project is compatible with the [DevOps-Orchestrator repo](https://github.com/vladbelo2/devops-orchestrator), allowing you to:
- 🧱 Spin VMs for any GitHub project with `vagrant up`
- 🐳 Launch Docker containers with custom base images, packages, and ports
- 🧠 Dynamically build or test games inside VM or container

---

## 🧪 Testing & Linting

Each game includes:
- ✅ `tests/` directory with PyTest-based test coverage
- 🔀 Testable in all environments (VM, Host, Docker, CI)
- ✅ Works even if some tests fail (`|| echo ...`)

---

## 🔐 Signing & Notarization

Currently skipped in CI. Future plans include:
- codesign and notarize for macOS
- signtool for Windows

---

## 🧠 How to Add Your Own Game

1. Create a folder in `games/your_game`
2. Add `main.py` and `assets.py` and `assets` folder
3. Create `build_config.json`
4. Append to `games.json`

You’ll get Docker builds, CI/CD, and native packages out of the box.

---

## 🔮 Roadmap: Future Phases

```text
Phase	Title	Status
✅	🎮 Game Dev Foundation	Complete
✅	🐳 Docker Builds	Complete
✅	🔁 GitHub Actions Matrix	Complete
✅	📦 Native Installers	Complete
🔜	☸️ Kubernetes Deployment	Planned
🔜	📊 Monitoring (Prometheus/Grafana)	Planned
🔜	🤖 Game Bots for Load Testing	Planned
🔜	💥 Chaos Engineering	Planned
🔜	🚀 GitOps with ArgoCD	Planned
🔜	🌐 Public Download Portal	Planned
```

---

## 📄 License

MIT License. See LICENSE.

---

## 🧑‍💻 Author

Vlad Belo 

DevOps Engineer | SRE | Automation Specialist
