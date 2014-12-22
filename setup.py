"""
py2app/py2exe build script for CounterParty GUI.

Usage (Mac OS X):
     python setup.py py2app

Usage (Windows):
     python setup.py py2exe

"""
import sys
from setuptools import setup

APP = ['counterpartygui.py']
DATA_FILES = ['core', 'plugins']

if sys.platform == 'darwin':
    extra_options = {
        'setup_requires': ['py2app'],
        'app': APP,
        'data_files': DATA_FILES,
        'options': {
            'py2app': {
                'argv_emulation': True, 
                'includes': ['sip', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtQml', 'PyQt5.QtNetwork'],
                'iconfile':'counterparty.icns',
                'plist': {
                    'CFBundleShortVersionString': '1.0',
                    'CFBundleGetInfoString': 'CounterParty GUI'
                }
            }
        }
    }
elif sys.platform == 'win32':
    extra_options = {
        'setup_requires': ['py2exe'],
        'app': APP,
        'data_files': DATA_FILES
    }
else:
    extra_options = {
        'scripts': APP,
        'data_files': DATA_FILES
    }
print(extra_options)

setup(
    name = 'counterpartygui',
    version = '1.0',
    author = 'Counterparty',
    **extra_options
)
