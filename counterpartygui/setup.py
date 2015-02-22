#!/usr/bin/env python

import os, sys
import shutil
import ctypes.util
import configparser, platform
import urllib.request
import tarfile, zipfile
import appdirs
import hashlib
from decimal import Decimal as D

def zip_folder(folder_path, zip_path):
    zip_file = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(folder_path):
        for a_file in files:
            zip_file.write(os.path.join(root, a_file))
    zip_file.close()

def before_py2exe_build(win_dist_dir):
    # Clean previous build
    if os.path.exists(win_dist_dir):
        shutil.rmtree(win_dist_dir)

    # py2exe don't manages entry_points
    with open('counterparty-gui.py', 'w+') as fp:
        exe_content = '''import os, sys
CURR_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser('__file__'))))
WIN_EXE_LIB = os.path.normpath(os.path.join(CURR_DIR, 'library'))
if os.path.isdir(WIN_EXE_LIB):
    sys.path.insert(0, WIN_EXE_LIB)
from counterpartygui.core.gui import main
main()'''
        fp.write(exe_content)

    # Hack
    src = 'C:\\Python34\\Lib\\site-packages\\flask_httpauth.py'
    dst = 'C:\\Python34\\Lib\\site-packages\\flask\\ext\\httpauth.py'
    shutil.copy(src, dst)

def after_py2exe_build(win_dist_dir):
    # clean temporaries scripts
    os.remove('counterparty-gui.py')

    # py2exe copies only pyc files in site-packages.zip
    # modules with no pyc files must be copied in 'dist/library/'
    import counterpartylib, counterpartygui, certifi
    additionals_modules = [counterpartylib, counterpartygui, certifi]
    for module in additionals_modules:
        module_file = os.path.dirname(module.__file__)
        dest_file = os.path.join(win_dist_dir, 'library', module.__name__)
        shutil.copytree(module_file, dest_file)

    # additionals DLLs
    dlls = ['ssleay32.dll', 'libssl32.dll', 'libeay32.dll']
    dlls.append(ctypes.util.find_msvcrt())
    dlls_path = dlls
    for dll in dlls:
        dll_path = ctypes.util.find_library(dll)
        shutil.copy(dll_path, win_dist_dir)

    # QT plugin
    src = 'C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins\\platforms\\qwindows.dll'
    os.makedirs(os.path.join(win_dist_dir, 'platforms'))
    dest = os.path.join(win_dist_dir, 'platforms', 'qwindows.dll')
    shutil.copy(src, dest)

    # QML Libraries
    qml_dir = 'C:\\Python34\\Lib\\site-packages\\PyQt5\\qml'
    for lib_dir in os.listdir(qml_dir):
        src = os.path.join(qml_dir, lib_dir)
        dst = os.path.join(win_dist_dir, lib_dir)
        shutil.copytree(src, dst)

    # compress distribution folder
    zip_path = '{}.zip'.format(win_dist_dir)
    zip_folder(win_dist_dir, zip_path)

    # Open,close, read file and calculate MD5 on its contents 
    with open(zip_path, 'rb') as zip_file:
        data = zip_file.read()    
        md5 = hashlib.md5(data).hexdigest()

    # include MD5 in the zip name
    new_zip_path = '{}-{}.zip'.format(win_dist_dir, md5)
    os.rename(zip_path, new_zip_path)

    # clean build folder
    #shutil.rmtree(win_dist_dir)

    # Clean Hack
    os.remove('C:\\Python34\\Lib\\site-packages\\flask\\ext\\httpauth.py')
