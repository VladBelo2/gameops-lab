from setuptools import setup
import os

print("🧪 [DEBUG] Running setup for Tetris...")

APP = ['main.py']
SDL_DYLIB = os.path.join(".dylibs", "libSDL2-2.0.0.dylib")

OPTIONS = {
    "argv_emulation": False,
    "packages": ["pygame"],
    "includes": ["pygame"],
    "iconfile": "assets/icon.icns",
    "resources": [SDL_DYLIB],  # ⬅️ Bundle SDL2 dylib
    "plist": {
        "CFBundleName": "Tetris",
        "CFBundleShortVersionString": "1.0",
        "CFBundleIdentifier": "com.example.tetris",
    },
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
