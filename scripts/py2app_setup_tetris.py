from setuptools import setup
import os

print("🧪 [DEBUG] Running setup for Tetris...")

APP = ['main.py']
OPTIONS = {
    "argv_emulation": True,
    "packages": ["pygame"],
    "includes": ["pygame"],
    "iconfile": "assets/icon.icns",
    "plist": {
        "CFBundleName": "Tetris",
        "CFBundleShortVersionString": "1.0",
        "CFBundleIdentifier": "com.example.tetris",
    },
    "resources": [],
    "frameworks": [],  # You can try adding SDL2 here if needed
}


setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
