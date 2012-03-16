import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QDir
from video import VideoFile

class MainWindow(QtGui.QMainWindow):
    video_file = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle("VSync")
        self.show()

        loadFileAction = QtGui.QAction("Load video...", self)
        loadFileAction.setShortcut("Ctrl+L")
        loadFileAction.triggered.connect(self.click_load_video)

        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(loadFileAction)
        self.status_ready()


    def click_load_video(self):
        filename = QtGui.QFileDialog().getOpenFileName(self, "Open video file", QDir.homePath())
        if filename == "":
            return      # User canceled the dialog

        self.statusBar().showMessage("Loading %s..." % (filename,))
        self.video_file = VideoFile(filename)
        self.status_ready()

    def status_ready(self):
        self.statusBar().showMessage("Ready.")

def main():
    """
    Main application entry point
    """
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()