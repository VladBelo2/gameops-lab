from setuptools import setup
import os

print("🧪 [DEBUG] Running setup for Brick Breaker...")

APP = ['main.py']
OPTIONS = {
    "argv_emulation": False,
    "packages": ["pygame"],
    "includes": ["pygame"],
    "iconfile": "assets/icon.icns",
    "plist": {
        "CFBundleName": "Brick Breaker",
        "CFBundleShortVersionString": "1.0",
        "CFBundleIdentifier": "com.example.brickbreaker",
    },
    "resources": [],
    "frameworks": [],  # You can try adding SDL2 here if needed
}


setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
