from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QMessageBox
from widgets.video_view import VideoView
from video import VideoFile, VideoException

class LoadVideoWindow(QtGui.QDialog):
    video = None

    def __init__(self, parent, video=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.setWindowTitle("Crop slide video")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)
        self.video = video

        self.video_view = VideoView(selectable=True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.video_view)

        self.ok_button = QtGui.QPushButton("OK")
        self.ok_button.clicked.connect(self._close)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def _close(self):
        if self.video_view.selected_box is not None:
            self.selected = self.video_view.selected_box
        else:
            self.selected = (0, 0, self.video.get_frame().width, self.video.get_frame().height)
        self.close()

    def showEvent(self, QShowEvent):
        if self.video is None:
            filename = QtGui.QFileDialog(self).getOpenFileName(self, "Open slide video file", QtCore.QDir.homePath())
            if filename == "":
                return      # User canceled the dialog

            try:
                video = VideoFile(filename)
            except VideoException as e:
                msgBox = QtGui.QMessageBox(QMessageBox.Critical, "Error :(", "Video file could not be opened.")
                msgBox.setDetailedText(unicode(e))
                msgBox.exec_()
                return

            self.video = video
            # Jump to middle of the video
            self.video.seek_to(self.video.get_info().duration / 2)

            timestamp, frame = self.video.get_frame()
            self.video_view.show_frame(frame)
