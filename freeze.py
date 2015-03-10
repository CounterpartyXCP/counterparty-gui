import os, sys, hashlib, shutil
import ctypes.util
from cx_Freeze import setup, Executable

import counterpartygui

# Check the presence, or update the path for folowing files
COUNTERPARTYLIB_PATH = 'C:\\counterparty\\counterpartyd\\counterpartylib'
CERTIFI_PEM_PATH = 'C:\\Python34\\Lib\\site-packages\\certifi-14.05.14-py3.4.egg\\certifi\\cacert.pem'
QML_LIBS_PATH = 'C:\\Python34\\Lib\\site-packages\\PyQt5\\qml'

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
        (CERTIFI_PEM_PATH, "certifi\\cacert.pem")
    ],
    "include_files": [
        ("servers.json", "servers.json"),
        ("plugins", "plugins"),
        ("assets", "assets"),
        ("i18n", "i18n"),
        (COUNTERPARTYLIB_PATH, "counterpartylib")
    ],
    "include_msvcr": True
}

# QML Libraries
for lib_dir in os.listdir(QML_LIBS_PATH):
    src = os.path.join(QML_LIBS_PATH, lib_dir)
    build_exe_options['include_files'].append((src, lib_dir))

# Additional DLL
for dll in ['d3dcompiler_47.dll', 'libEGL.dll', 'libGLESv2.dll', 'msvcr110.dll', 'msvcp110.dll']:
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

if sys.platform == "win32":
    dist_path = 'dist/counterparty-gui-{}-amd64.msi'.format(counterpartygui.APP_VERSION)
    new_dist_path = 'dist/counterparty-gui-{}-amd64-{}.msi'

# Open,close, read file and calculate MD5 on its contents  
with open(dist_path, 'rb') as dist_file:
    data = dist_file.read()    
    md5 = hashlib.md5(data).hexdigest()
# Include the MD5 in the distribution filename
new_dist_path = new_dist_path.format(counterpartygui.APP_VERSION + '-BETA', md5) # distutils does not support BETA
shutil.copy(dist_path, new_dist_path) # renaming raises a PermissionError (?)