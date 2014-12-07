from PyQt5.QtWidgets import QApplication

from lib.gui import GUI
from lib.config import Config

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    config = Config()
    screen = GUI(config)

    
    sys.exit(app.exec_())