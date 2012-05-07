import logging
import multiprocessing
import sys
from PyQt4 import QtGui
from windows.main_window import MainWindow

logger = logging.getLogger(__name__)

def main():
    """
    Main application entry point
    """
    logging.basicConfig(level=logging.DEBUG)

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()