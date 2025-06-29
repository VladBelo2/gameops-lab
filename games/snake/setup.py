from setuptools import setup

APP = ['main.py']
DATA_FILES = ['assets']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'iconfile': 'assets/default-icon.icns'  # optional
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
