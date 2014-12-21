#! /usr/bin/env python3
from PyQt5.QtWidgets import QApplication

from core.gui import GUI
from core.config import Config

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    config = Config()
    screen = GUI(config)
    
    sys.exit(app.exec_())