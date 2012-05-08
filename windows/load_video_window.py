from PyQt4 import QtGui
from widgets.video_view import VideoView

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
            self.selected = (0, 0, self.video.get_frame()[1].width, self.video.get_frame()[1].height)
        self.close()

    def showEvent(self, QShowEvent):
        # Jump to middle of the video
        self.video.seek_to(self.video.get_info().duration / 2)
        timestamp, frame = self.video.get_frame()
        self.video_view.show_frame(frame)
