"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['hnreader.py']
DATA_FILES = ['template.html', 'yhn.png']
OPTIONS = {'argv_emulation': True, 'includes': 'lxml._elementpath', 'packages': 'pygments'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
