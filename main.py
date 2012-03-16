import sys
from PyQt4 import QtGui

def main():
    """
    Main application entry point
    """
    app = QtGui.QApplication(sys.argv)

    widget= QtGui.QWidget()
    widget.resize(250, 150)
    widget.move(300, 300)
    widget.setWindowTitle("Yay okno!")
    widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()