import os, sys
import ctypes.util
from cx_Freeze import setup, Executable

import counterpartygui

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "excludes": ['counterpartylib'],
    "packages": [
        'PyQt5.QtNetwork',
        'colorlog',
        'apsw',
        'sha3',
        'bitcoin',
        'logging',
        'flask',
        'flask_httpauth',
        'tornado',
        'jsonrpc',
        'appdirs',
        'dateutil',
        'tendo',
        'xmltodict',
        'pycoin',
        'Crypto'
    ],
    "zip_includes": [
        ("C:\\Python34\\Lib\\site-packages\\certifi-14.05.14-py3.4.egg\\certifi\\cacert.pem", "certifi\\cacert.pem")
    ],
    "include_files": [
        ("servers.json", "servers.json"),
        ("plugins", "plugins"),
        ("assets", "assets"),
        ("i18n", "i18n"),
        ("C:\\counterparty\\counterpartyd\\counterpartylib", "counterpartylib")
    ],
    "include_msvcr": True
}

# QML Libraries
qml_dir = 'C:\\Python34\\Lib\\site-packages\\PyQt5\\qml'
for lib_dir in os.listdir(qml_dir):
    src = os.path.join(qml_dir, lib_dir)
    build_exe_options['include_files'].append((src, lib_dir))

# Additional DLL
for dll in ['d3dcompiler_47.dll', 'libEGL.dll', 'libGLESv2.dll']:
    dll_path = ctypes.util.find_library(dll)
    build_exe_options['include_files'].append((dll_path, dll))

base = None
if sys.platform == "win32":
    base = "Win32GUI"

shortcut_table = [(
    "DesktopShortcut",                  # Shortcut
    "DesktopFolder",                    # Directory_
    "Counterparty GUI",                 # Name
    "TARGETDIR",                        # Component_
    "[TARGETDIR]counterparty-gui.exe",  # Target
    None,                               # Arguments
    None,                               # Description
    None,                               # Hotkey
    None,                               # Icon
    0,                                  # IconIndex
    None,                               # ShowCmd
    'TARGETDIR'                         # WkDir
), (
    "ProgramMenuShortcut",              # Shortcut
    "ProgramMenuFolder",                # Directory_
    "Counterparty GUI",                 # Name
    "TARGETDIR",                        # Component_
    "[TARGETDIR]counterparty-gui.exe",  # Target
    None,                               # Arguments
    None,                               # Description
    None,                               # Hotkey
    None,                               # Icon
    0,                                  # IconIndex
    None,                               # ShowCmd
    'TARGETDIR'                         # WkDir
)]

bdist_msi_options = {'data': {"Shortcut": shortcut_table}}
    
setup_options = {
    'name': counterpartygui.APP_NAME,
    'version': counterpartygui.APP_VERSION,
    'options': {
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    'executables': [Executable("counterparty-gui.py", base=base, icon="assets/counterparty.ico")]
}

setup(**setup_options)
