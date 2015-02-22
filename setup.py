import sys
from setuptools import setup, find_packages

APP_VERSION = "1.0.0"

# TODO: make dynamic
data_files =  {
    '': ['plugins/send/*.*', 'plugins/test/*.*', 'assets/*.*']
}    

required_packages = [
    'appdirs',
    'counterparty-cli'
]

setup_options = {
    'name': 'counterparty-gui',
    'version': APP_VERSION,
    'author': 'Counterparty Foundation',
    'author_email': 'support@counterparty.io',
    'maintainer': 'Ouziel Slama',
    'maintainer_email': 'ouziel@counterparty.io',
    'url': 'http://counterparty.io',
    'license': 'MIT',
    'description': 'Counterparty Wallet',
    'long_description': '',
    'keywords': 'counterparty,bitcoin',
    'classifiers': [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Office/Business :: Financial",
        "Topic :: System :: Distributed Computing"
    ],
    'download_url': 'https://github.com/CounterpartyXCP/counterparty-gui/releases/tag/v' + APP_VERSION,
    'provides': ['counterpartygui'],
    'packages': find_packages(),
    'include_package_data': True,
    'package_data': data_files,
    'zip_safe': False,
    'install_requires': required_packages,
    'entry_points': {
        'gui_scripts': [
            'counterparty-gui = counterpartygui.core.gui:main'
        ]
    }
}

if sys.argv[1] == 'py2exe':
    import py2exe
    from py2exe.distutils_buildexe import py2exe as _py2exe

    WIN_DIST_DIR = 'counterparty-gui-win32-{}'.format(APP_VERSION)
    
    class py2exe(_py2exe):
        def run(self):
            from counterpartygui.setup import before_py2exe_build, after_py2exe_build
            # prepare build
            before_py2exe_build(WIN_DIST_DIR)
            # build exe's
            _py2exe.run(self)
            # tweak build
            after_py2exe_build(WIN_DIST_DIR)

    # Update setup_options with py2exe specifics options
    setup_options.update({
        'console': [
            'counterparty-gui.py'
        ],
        'zipfile': 'library/site-packages.zip',
        'options': {
            'py2exe': {
                'dist_dir': WIN_DIST_DIR,
                'includes': ['sip', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtQml', 'PyQt5.QtNetwork', 'PyQt5.QtQuick', 'PyQt5.QtQuickWidgets']
            }
        },
        'cmdclass': {
            'py2exe': py2exe
        }
    })

setup(**setup_options)
