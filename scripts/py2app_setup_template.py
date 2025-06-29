from setuptools import setup

APP = ['main.py']
DATA_FILES = [('assets', ['assets/DejaVuSans.ttf'])]

OPTIONS = {
    'argv_emulation': True,
    'packages': ['pygame'],
    'excludes': ['PySide2', 'gi', 'Gst', 'GstBase', 'GstInsertBin', 'GstBadAudio'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
