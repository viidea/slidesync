from PyQt4 import QtGui
from PyQt4.QtGui import QImage, QLabel

class VideoView(QLabel):
    current_image = None        # Used for resizing

    def __init__(self):
        super(QLabel, self).__init__()

    def show_frame(self, video_frame):
        assert video_frame.format == "RGB"
        self.current_image = QImage(video_frame.data, video_frame.width, video_frame.height, QImage.Format_RGB888)
        self.update()

    def resizeEvent(self, resize_event):
        super(QLabel, self).resizeEvent(resize_event)
        if resize_event.oldSize() != resize_event.size():
            self.update()

    def update(self):
        super(QLabel, self).update()

        if self.current_image is not None:
            self.setPixmap(QtGui.QPixmap.fromImage(self.current_image.scaledToWidth(self.width())))