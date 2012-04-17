from PyQt4 import QtGui
from widgets.video_view import VideoView

class CropWindow(QtGui.QDialog):
    _video = None

    def __init__(self, video):
        super(CropWindow, self).__init__()
        self.setWindowTitle("Crop slide video")
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        self._video = video

        self.video_view = VideoView(selectable=True)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.video_view)

        self.ok_button = QtGui.QPushButton("OK")
        self.ok_button.clicked.connect(self._close)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        time, frame = video.get_frame()
        assert frame is not None
        self.video_view.show_frame(frame)

    def _close(self):
        if self.video_view.selected_box is not None:
            self.selected = self.video_view.selected_box
        else:
            self.selected = (0, 0, self._video.get_frame().width, self._video.get_frame().height)
        self.close()