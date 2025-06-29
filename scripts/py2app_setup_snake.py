from setuptools import setup

APP = ['main.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'assets/icon.icns',
    'packages': ['pygame'],
    'plist': {
        'CFBundleName': 'Snake',
        'CFBundleIdentifier': 'com.gameopslab.snake',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleExecutable': 'snake',
    }
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
