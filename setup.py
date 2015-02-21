import sys
from setuptools import setup, find_packages

APP_VERSION = "1.0.0"

# TODO: make dynamic
data_files =  {
    '': ['plugins/send/*.*', 'plugins/test/*.*']
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

setup(**setup_options)
