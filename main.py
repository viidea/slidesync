import logging
import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QDir, Qt, QString
from PyQt4.QtGui import QMessageBox
import video

logger = logging.getLogger(__name__)

class MainWindow(QtGui.QMainWindow):
    video_file = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle("VSync")

        # Prepare toolbar
        loadFileAction = QtGui.QAction("Load video...", self)
        loadFileAction.setShortcut("Ctrl+L")
        loadFileAction.triggered.connect(self.click_load_video)
        self.toolbar = self.addToolBar("Main")
        self.toolbar.addAction(loadFileAction)

        # Prepare status bar
        self.status_label = QtGui.QLabel("Status")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.statusBar().addWidget(self.status_label, stretch=1)

        self.video_label = QtGui.QLabel("")
        self.video_label.setMinimumWidth(150)
        self.video_label.setAlignment(Qt.AlignRight)
        self.statusBar().addWidget(self.video_label)
        self.status_ready()

        self.show()

    def click_load_video(self):
        filename = QtGui.QFileDialog().getOpenFileName(self, "Open video file", QDir.homePath())
        if filename == "":
            return      # User canceled the dialog

        self.status_label.setText("Loading %s..." % (filename,))

        try:
            self.video_file = video.VideoFile(filename)
        except video.VideoException as e:
            msgBox = QMessageBox(QMessageBox.Critical, "Error :(", "Video file could not be opened.")
            msgBox.setDetailedText(unicode(e))
            msgBox.exec_()
            return

        self.status_ready()
        self.video_label.setText(unicode(self.video_file.get_info()))

    def status_ready(self):
        self.status_label.setText("Ready.")
        self.status_label.update()

def main():
    """
    Main application entry point
    """
    logging.basicConfig()

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()