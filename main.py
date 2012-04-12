import logging
import sys
from PyQt4 import QtGui
from main_window import MainWindow

logger = logging.getLogger(__name__)

def main():
    """
    Main application entry point
    """
    logging.basicConfig(level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()