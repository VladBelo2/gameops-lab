from setuptools import setup
import os

print("🧪 [DEBUG] Running setup for Brick Breaker...")

APP = ['main.py']
OPTIONS = {
    "argv_emulation": True,
    "packages": ["pygame"],
    "includes": [],
    "excludes": [],
    "resources": [],
    "frameworks": [],
    "iconfile": "assets/icon.icns",
    "plist": {
        "CFBundleName": "Brick Breaker",
        "CFBundleShortVersionString": "1.0",
        "CFBundleIdentifier": "com.example.brickbreaker",
    },
    "includes": ["pygame"],
    "include_patterns": ["libSDL2*"],
}


setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
