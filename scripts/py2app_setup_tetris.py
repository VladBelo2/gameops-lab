from setuptools import setup
import os

print("🧪 [DEBUG] Running setup for Tetris...")

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': os.path.join('assets', 'icon.icns'),
    'packages': ['pygame'],
    'plist': {
        'CFBundleName': 'Tetris',
        'CFBundleIdentifier': 'com.gameopslab.tetris',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'tetris',
    }
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
